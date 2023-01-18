import json
from typing import Any, Callable

from flask_socketio import SocketIO

from jianmu.pyvar.AbstractRef import AbstractRef
from jianmu.pyvar.Proxy import Proxy
from jianmu.pyvar.utils import unref


class Ref(AbstractRef):
    socketio: 'SocketIO | None' = None
    __proxy: Proxy
    __name: str
    __event_name: str
    __registered: bool

    def __init__(self, value: Any, name: str = ''):
        value = unref(value)
        try:
            json.dumps(value)
        except Exception as e:
            raise RuntimeError('The value cannot be serialized to JSON') from e
        self.__proxy = Proxy(value)
        self.__registered = False
        if name:
            self.register(name)

    def __set_value(self, value, trigger_change_handlers: bool = True):
        value = unref(value)
        if trigger_change_handlers:
            self.__proxy.value = value
        else:
            self.__proxy.set_value_without_triggering_change_handlers(value)

    def json(self, **kwargs):
        return json.dumps(self.__proxy.value, **kwargs)

    def register(self, name: str):
        self.__name = name
        self.__event_name = f'pyvar_{name}'
        self.__init_socketio_handler()
        self.add_change_handler(self.__update_value_to_frontend)
        self.__registered = True

    def add_change_handler(self, handler: 'Callable[[], None] | Callable[[Any], None] | Callable[[Any, Any], None]'):
        self.__proxy.add_change_handler(handler)

    def __update_value_to_frontend(self):
        if Ref.socketio is None:
            raise RuntimeError('The socketio is not initialized')
        if self.__registered:
            Ref.socketio.emit(self.__event_name, {
                'data': self.__proxy.value,
            })

    def __notify_synced_to_frontend(self):
        if Ref.socketio is None:
            raise RuntimeError('The socketio is not initialized')
        if self.__registered:
            Ref.socketio.emit(f'{self.__event_name}__synced')

    def __init_socketio_handler(self):
        if Ref.socketio is None:
            raise RuntimeError('The socketio is not initialized')

        @Ref.socketio.on(self.__event_name)
        def on_pyvar_change(res: 'dict[str, Any]'):
            if 'data' not in res:
                raise RuntimeError('The data field is missing')
            value = res['data']
            self.__set_value(value, trigger_change_handlers=False)
            self.__notify_synced_to_frontend()

        @Ref.socketio.on(f'{self.__event_name}__get')
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
        val = unref(value)
        try:
            json.dumps(val)
        except Exception as e:
            raise RuntimeError(f'{self.__name}: The value cannot be serialized to JSON') from e
        self.__set_value(val)

    def __repr__(self):
        return (f'<Ref {self.__name}={self.__proxy.value}>' if self.__registered else f'<Ref {self.__proxy.value}>')
