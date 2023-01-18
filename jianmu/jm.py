# sourcery skip: avoid-builtin-shadow
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)  # Set stdout to unbuffered mode
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf8', buffering=1)  # Set stderr to unbuffered mode

from inspect import signature
from pathlib import Path
from typing import Any, Callable, Dict, List

from flask import Flask, request
from flask_socketio import SocketIO

from jianmu.datatypes import JSONValue
from jianmu.exceptions import JianmuException
from jianmu.info import jianmu_info
import jianmu.pyvar as pyvar_module
from jianmu.pyvar import init_pyvar_socketio, register_pyvar, Ref, get_registered_pyvars, AbstractRef

CWD = str(Path.cwd())
if CWD not in sys.path:
    sys.path.insert(0, CWD)
SRC = str(Path.cwd() / 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

flask_app = Flask(__name__)
socketio = SocketIO(flask_app, cors_allowed_origins='*')
init_pyvar_socketio(socketio)

from src import app  # type: ignore


@flask_app.route('/')
def index():
    return '<h1>Powered by Jianmu Framework</h1>'


def get_info():
    return jianmu_info, '获取程序信息成功'


def registered_pyvars():
    return get_registered_pyvars(), '获取已注册的响应式变量成功'


def respond(error: int, message: str, data: JSONValue) -> Dict[str, Any]:
    return {
        'error': error,
        'message': message,
        'data': data,
    }


def wrapper(func: Callable):

    def view_func():
        sys.stdout.write(f'Function {func.__name__} is called.\n')
        try:
            param_num = len(signature(func).parameters)
            json = request.get_json()
            if json is None:
                raise JianmuException('The Content-Type header is not application/json')
            args: List[Any] = json
            if param_num:
                if not args:
                    raise JianmuException('The argument is empty')
                if param_num != len(args):
                    raise JianmuException('The number of arguments do not match')
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


if __name__ == '__main__':
    for key, val in app.__dict__.items():
        if key[:2] != '__':
            if isinstance(val, AbstractRef):  # Reactive Variable
                var_name = key
                var = val
                register_pyvar(var, var_name)
                sys.stderr.write(f'Reactive Variable {var_name} is registered.\n')
            elif callable(val):  # Python Function
                if isinstance(val, type):
                    continue
                func_name = key
                func = val
                if func_name in pyvar_module.__dict__:
                    continue
                rule = f'/api/{func_name}'
                view_func = wrapper(func)
                sys.stderr.write(f'Python Function {func_name} is registered.\n')
                flask_app.add_url_rule(rule, func_name, view_func, methods=['POST'])
    flask_app.add_url_rule('/api/info', 'info', wrapper(get_info), methods=['POST'])
    flask_app.add_url_rule('/api/registered_pyvars', 'registered_pyvars', wrapper(registered_pyvars), methods=['POST'])
    # http_server = WSGIServer(('127.0.0.1', 19020), flask_app)
    # http_server.serve_forever()
    # Use socketio.run() instead of http_server.serve_forever() to enable
    socketio.run(flask_app, host='127.0.0.1', port=19020)
