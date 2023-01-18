import inspect
import json
from typing import Any, Callable, List

from flask_socketio import SocketIO

from jianmu.pyvar.AbstractRef import AbstractRef
from jianmu.pyvar.Proxy import Proxy
from jianmu.pyvar.Ref import Ref
from jianmu.pyvar.utils import unref


class ComputedRef(AbstractRef):
    socketio: 'SocketIO | None' = None
    __deps: 'List[AbstractRef]'
    __func: Callable[[], Any]
    __proxy: Proxy
    __name: str
    __event_name: str
    __registered: bool

    def __init__(self, func: Callable[[], Any], name: str = ''):
        value = unref(func())
        try:
            json.dumps(value)
        except Exception as e:
            raise RuntimeError('The value cannot be serialized to JSON') from e
        self.__func = func
        self.__deps = self.__get_deps(func)
        self.__proxy = Proxy(value)
        self.__registered = False
        if name:
            self.register(name)

    def __get_deps(self, func: Callable[[], Any]) -> 'List[AbstractRef]':
        closure_vars = inspect.getclosurevars(func)
        nonlocal_vars = closure_vars.nonlocals
        global_vars = closure_vars.globals
        return [v for v in {**nonlocal_vars, **global_vars}.values() if isinstance(v, AbstractRef)]

    def json(self, **kwargs):
        return json.dumps(self.__proxy.value, **kwargs)

    def register(self, name: str):
        self.__name = name
        self.__event_name = f'pyvar_{name}'
        self.__init_socketio_handler()
        self.add_change_handler(self.__update_value_to_frontend)
        for dep in self.__deps:
            dep.add_change_handler(self.__update_value)
        self.__registered = True

    def add_change_handler(self, handler: 'Callable[[], None] | Callable[[Any], None] | Callable[[Any, Any], None]'):
        self.__proxy.add_change_handler(handler)

    def __update_value(self):
        value = unref(self.__func())
        if value != self.__proxy.value:
            self.__proxy.value = value

    def __update_value_to_frontend(self):
        if ComputedRef.socketio is None:
            raise RuntimeError('The socketio is not initialized')
        if self.__registered:
            ComputedRef.socketio.emit(self.__event_name, {
                'data': self.__proxy.value,
            })

    def __init_socketio_handler(self):
        if ComputedRef.socketio is None:
            raise RuntimeError('The socketio is not initialized')

        # @ComputedRef.socketio.on(self.__event_name)
        # def on_pyvar_change(res: 'dict[str, Any]'):
        #     raise RuntimeError('The value of a ComputedRef cannot change')

        @ComputedRef.socketio.on(f'{self.__event_name}__get')
        def on_pyvar_get():
            self.__update_value_to_frontend()

        self.__update_value_to_frontend()

    @property
    def value(self) -> Proxy:
        return self.__proxy

    @property
    def true_value(self) -> Any:
        return self.__proxy.value

    @value.setter
    def value(self, value: Any):
        raise RuntimeError('The value of a ComputedRef cannot be set')

    def __repr__(self):
        return (f'<ComputedRef {self.__name}={self.__proxy.value}>'
                if self.__registered else f'<ComputedRef {self.__proxy.value}>')
