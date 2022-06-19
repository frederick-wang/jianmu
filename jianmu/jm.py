import sys
from inspect import signature
from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence, Union

from exceptions import JianmuException
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from info import jianmu_info

CWD = str(Path.cwd())
if CWD not in sys.path:
    sys.path.insert(0, CWD)
SRC = str(Path.cwd() / 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from src import app

flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    return '<h1>Powered by Jianmu Framework</h1>'


def get_info():
    return jianmu_info, '获取程序信息成功'


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
        sys.stdout.write(f'Function {func.__name__} is called.\n')
        sys.stdout.flush()
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
            sys.stderr.write(f'Function {func_name} is registered.\n')
            sys.stderr.flush()
            flask_app.add_url_rule(rule, func_name, view_func, methods=['POST'])
    flask_app.add_url_rule('/api/info',
                           'info',
                           wrapper(get_info),
                           methods=['POST'])
    http_server = WSGIServer(('127.0.0.1', 19020), flask_app)
    http_server.serve_forever()
