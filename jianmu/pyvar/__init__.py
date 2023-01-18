from typing import Any, Callable, Dict

from flask_socketio import SocketIO

from jianmu.pyvar.AbstractRef import AbstractRef
from jianmu.pyvar.ComputedRef import ComputedRef
from jianmu.pyvar.Ref import Ref


def init_pyvar_socketio(_socketio: 'SocketIO'):
    Ref.socketio = _socketio
    ComputedRef.socketio = _socketio


__registered_pyvars: Dict[str, 'AbstractRef'] = {}


def get_registered_pyvars() -> 'list[str]':
    return list(__registered_pyvars.keys())


def register_pyvar(value: AbstractRef, name: str) -> None:
    value.register(name)
    __registered_pyvars[name] = value


def ref(value: Any) -> Ref:
    return Ref(value)


def computed(func: Callable[[], Any]) -> ComputedRef:
    return ComputedRef(func)
