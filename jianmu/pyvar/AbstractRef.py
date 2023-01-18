from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Any, Callable


class AbstractRef(metaclass=ABCMeta):

    @abstractproperty
    def value(self) -> Any:
        pass

    @abstractproperty
    def true_value(self) -> Any:
        pass

    @abstractmethod
    def json(self, **kwargs) -> str:
        pass

    @abstractmethod
    def register(self, name: str) -> None:
        pass

    @abstractmethod
    def add_change_handler(self,
                           handler: 'Callable[[], None] | Callable[[Any], None] | Callable[[Any, Any], None]') -> None:
        pass
