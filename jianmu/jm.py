# sourcery skip: avoid-builtin-shadow
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)  # Set stdout to unbuffered mode
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf8', buffering=1)  # Set stderr to unbuffered mode

import base64
import contextlib
import os
from inspect import signature
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, List, Set

import reactivity as reactivity_module
from flask import Flask, request
from reactivity import Ref, is_computed_ref, is_ref, to_raw, watch

import jianmu as jianmu_module
from jianmu.datatypes import JSONValue
from jianmu.definitions import File
from jianmu.exceptions import JianmuException
from jianmu.info import jianmu_info
from jianmu.sock import get_socketio, init_socketio
from jianmu.utils import datauri_to_bytes

flask_app = Flask(__name__)
init_socketio(flask_app)
socketio = get_socketio()

src_modules: Dict[str, ModuleType] = {}

for module_name in os.listdir(Path.cwd()):
    if module_name.endswith('.py') and os.path.isfile(module_name):
        module_name = module_name[:-3]
    if module_name.startswith('__') and module_name.endswith('__'):
        continue
    with contextlib.suppress(ImportError):
        module = __import__(f'src.{module_name}', fromlist=(module_name,))
        sys.modules[module_name] = module
        del sys.modules[f'src.{module_name}']
        src_modules[module_name] = module

# Check if the default entry point (app) exists.
if 'app' not in src_modules:
    raise ImportError(
        'No app.py found in the src directory. Please create one. You must have a file named app.py in the src directory as the default entry point of your app.'
    )

# Add all members of reactivity and jianmu to builtin_member_ids and then ignore them.
builtin_member_ids: Set[int] = {id(member) for member in reactivity_module.__dict__.values()}
builtin_member_ids.update({id(member) for member in jianmu_module.__dict__.values()})
registered_id_map: Dict[int, Any] = {}
'''Map from id in memory to its instance.'''
registered_name_map: Dict[str, Any] = {}
'''Map from name (var, func) to its instance'''


def is_sync_object(obj: Any) -> bool:
    # If obj is Dict, and obj has 'protocol', 'version', 'source', 'type', 'data' keys, it is a sync object.
    return isinstance(
        obj, dict) and 'protocol' in obj and 'version' in obj and 'source' in obj and 'type' in obj and 'data' in obj


def sync_file_data_to_file(file_data: Dict[str, Any]) -> File:
    return File(
        lastModified=file_data['lastModified'],
        name=file_data['name'],
        bytes=datauri_to_bytes(file_data['base64Src']),
        path=file_data['path'],
        size=file_data['size'],
        type=file_data['type'],
        webkitRelativePath=file_data['webkitRelativePath'],
    )


def file_to_sync_file_data(file: File) -> Dict[str, Any]:
    base64Src = f'data:{file.type};base64,{base64.b64encode(file.bytes).decode()}'
    return {
        'lastModified': file.lastModified,
        'name': file.name,
        'base64Src': base64Src,
        'path': file.path,
        'size': file.size,
        'type': file.type,
        'webkitRelativePath': file.webkitRelativePath,
    }


def sync_object_to_py_data(obj: Any) -> Any:
    # obj is json object
    if is_sync_object(obj):
        if obj['type'] == 'File':
            return sync_file_data_to_file(obj['data'])
        else:
            raise JianmuException(f'Unknown sync object type: {obj["type"]}')
    elif isinstance(obj, list):
        return [sync_object_to_py_data(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: sync_object_to_py_data(value) for key, value in obj.items()}
    return obj


def py_data_to_sync_data(obj: Any) -> Any:
    if isinstance(obj, File):
        return {
            'protocol': 'jianmu-object-sync-protocol',
            'version': 1,
            'source': 'javascript',
            'type': 'File',
            'data': file_to_sync_file_data(obj),
        }
    elif isinstance(obj, list):
        return [py_data_to_sync_data(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: py_data_to_sync_data(value) for key, value in obj.items()}
    return obj


@flask_app.route('/')
def index():
    return '<h1>Powered by Jianmu Framework</h1>'


def get_info():
    return jianmu_info, '获取程序信息成功'


@flask_app.route('/__jianmu_api__/heartbeat', methods=['GET'])
def heartbeat():
    return 'ok'


def respond(error: int, message: str, data: JSONValue) -> Dict[str, Any]:
    return {
        'error': error,
        'message': message,
        'data': data,
    }


def wrapper(func_name: str, func: Callable):

    def view_func():
        sys.stdout.write(f'Function {func_name} is called.\n')
        try:
            param_num = len(signature(func).parameters)
            json = request.get_json()
            if json is None:
                raise JianmuException('The Content-Type header is not application/json')
            args: List[Any] = json
            args_num = len(args)
            if param_num:
                if not args:
                    raise JianmuException('The argument is empty')
                if param_num != args_num:
                    args = [args[i] if i < args_num else None for i in range(param_num)]
                data = func(*args)
            else:
                data = func()
            if isinstance(data, tuple):
                if not data:
                    return respond(0, '', None)
                if len(data) == 1:
                    return respond(0, '', data[0])
                if len(data) > 2:
                    raise JianmuException('The number of return values is greater than 2')
                return respond(0, data[1], data[0])
            return respond(0, '', data)
        except Exception as e:
            return respond(1, e.args[0], None) if e.args else respond(1, str(e), None)

    return view_func


def register_reactive_var(name: str, var: Ref):
    event_name = f'pyvar_{name}'
    GET_PY_VALUE = f'{event_name}__get_py_value'
    PUSH_PY_TO_JS = f'{event_name}__push_py_to_js'
    PUSH_JS_TO_PY = f'{event_name}__push_js_to_py'
    PY_SYNCED_WITH_JS = f'{event_name}__py_synced_with_js'
    JS_SYNCED_WITH_PY = f'{event_name}__js_synced_with_py'
    is_computed = is_computed_ref(member)

    is_syncing = False

    latest_pushed_py_value = None

    def set_sync_status_to_syncing():
        nonlocal is_syncing
        is_syncing = True

    @socketio.on(JS_SYNCED_WITH_PY)
    def set_sync_status_to_synced():
        nonlocal is_syncing
        is_syncing = False
        if latest_pushed_py_value != to_raw(var.value):
            push_py_to_js()

    @socketio.on(GET_PY_VALUE)
    def push_py_to_js():
        nonlocal latest_pushed_py_value
        if not is_syncing:
            set_sync_status_to_syncing()
            socketio.emit(PUSH_PY_TO_JS, {'data': py_data_to_sync_data(var.value)})
            latest_pushed_py_value = to_raw(var.value)

    @socketio.on(PUSH_JS_TO_PY)
    def sync_py_with_js(res: 'dict[str, Any]'):
        if is_computed:
            socketio.emit(PY_SYNCED_WITH_JS)
            return
        if 'data' not in res:
            raise RuntimeError('The data field is missing')
        value = res['data']
        set_sync_status_to_syncing()
        var.value = sync_object_to_py_data(value)
        set_sync_status_to_synced()
        socketio.emit(PY_SYNCED_WITH_JS)

    watch(var, push_py_to_js, deep=True)


def register_member(module_name: str, member_name: str, member: Any):
    member_id = id(member)
    if member_id in builtin_member_ids:
        return
    member_fullname = f'{module_name}.{member_name}'
    if is_ref(member):  # Reactive Variable
        # TODO: 暂时不支持变量的多名称注册
        if member_id in registered_id_map:
            return
        register_reactive_var(member_fullname, member)
        registered_id_map[member_id] = member
        registered_name_map[member_fullname] = member
        sys.stderr.write(f'Reactive Variable {member_fullname} is registered.\n')
    elif callable(member):  # Python Function
        if isinstance(member, type):
            return
        rule = f'/api/{member_fullname}'
        if member_id in registered_id_map:
            view_func = registered_id_map[member_id]
        else:
            view_func = wrapper(member_fullname, member)
            registered_id_map[member_id] = view_func
            registered_name_map[member_fullname] = view_func
        flask_app.add_url_rule(rule, member_fullname, view_func, methods=['POST'])
        sys.stderr.write(f'Python Function {member_fullname} is registered.\n')


if __name__ == '__main__':
    for module_name, module in src_modules.items():
        for member_name, member in module.__dict__.items():
            if member_name[:2] == '__':
                continue
            register_member(module_name, member_name, member)

    flask_app.add_url_rule('/api/info', 'info', wrapper('info', get_info), methods=['POST'])
    socketio.run(flask_app, host='127.0.0.1', port=19020)
