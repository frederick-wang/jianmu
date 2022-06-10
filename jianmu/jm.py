import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence, Union
from inspect import signature
from flask import Flask, request
from exceptions import JianmuException

CWD = str(Path.cwd())
if CWD not in sys.path:
    sys.path.insert(0, CWD)

from src import app

server = Flask(__name__)


@server.route('/')
def index():
    return '<h1>Powered by Jianmu Framework</h1>'


def get_info():
    data = {
        'executable': sys.executable,
        'version': sys.version,
        'versionInfo': sys.version_info,
        'executableDir': str(Path(sys.executable).parent.resolve().absolute()),
        'currentDir': str(Path(__file__).parent.resolve().absolute()),
        'platform': sys.platform,
        'cwd': str(Path.cwd().resolve().absolute()),
    }
    return data, '获取程序信息成功'


JSONValue = Union[str, int, float, bool, None, Dict[str, 'JSONValue'],
                  Sequence['JSONValue']]


def respond(error: int, message: str, data: JSONValue) -> Dict[str, Any]:
    return {
        'error': error,
        'message': message,
        'data': data,
    }


def wrapper(func: Callable):

    def view_func():
        try:
            param_num = len(signature(func).parameters)
            json = request.get_json()
            if json is None:
                raise JianmuException(
                    'The Content-Type header is not application/json')
            args: List[Any] = json
            if param_num:
                if not args:
                    raise JianmuException('The argument is empty')
                if param_num != len(args):
                    raise JianmuException(
                        'The number of arguments do not match')
                data = func(*args)
            else:
                data = func()
            if isinstance(data, tuple):
                if not data:
                    return respond(0, '', None)
                if len(data) == 1:
                    return respond(0, '', data[0])
                if len(data) > 2:
                    raise JianmuException(
                        'The number of return values is greater than 2')
                return respond(0, data[1], data[0])
            return respond(0, '', data)
        except Exception as e:
            return respond(1, e.args[0], None) if e.args else respond(
                1, str(e), None)

    return view_func


if __name__ == '__main__':
    for key, val in app.__dict__.items():
        if key[:2] != '__' and callable(val):
            func_name = key
            func = val
            rule = f'/api/{func_name}'
            view_func = wrapper(func)
            print(f' * [add_url_rule: rule={rule}, func={func_name}]')
            server.add_url_rule(rule, func_name, view_func, methods=['POST'])
    server.add_url_rule('/api/info',
                        'info',
                        wrapper(get_info),
                        methods=['POST'])
    server.run(port=19020, host='0.0.0.0', debug=True)
