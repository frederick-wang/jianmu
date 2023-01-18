import inspect
from typing import Any, Callable, cast

from jianmu.pyvar.utils import unref


class Proxy:
    __value: Any
    __change_handlers: 'list[Callable[[], None] | Callable[[Any], None] | Callable[[Any, Any], None]]'

    def __init__(self, value: Any):
        self.__value = unref(value)
        self.__change_handlers = []

    def add_change_handler(self, handler: 'Callable[[], None] | Callable[[Any], None] | Callable[[Any, Any], None]'):
        if handler not in self.__change_handlers:
            self.__change_handlers.append(handler)

    def remove_change_handler(self, handler: 'Callable[[], None] | Callable[[Any], None] | Callable[[Any, Any], None]'):
        self.__change_handlers.remove(handler)

    def clear_change_handlers(self):
        self.__change_handlers.clear()

    def __invoke_change_handlers(self, new_value: Any, old_value: Any):
        for handler in self.__change_handlers:
            if len(inspect.signature(handler).parameters) == 0:
                handler = cast(Callable[[], None], handler)
                handler()
            elif len(inspect.signature(handler).parameters) == 1:
                handler = cast(Callable[[Any], None], handler)
                handler(new_value)
            else:
                handler = cast(Callable[[Any, Any], None], handler)
                handler(new_value, old_value)

    def __del__(self):
        self.__value = None
        self.__change_handlers = []

    def __repr__(self):
        return repr(self.__value)

    def __str__(self):
        return str(self.__value)

    def __bytes__(self):
        return bytes(self.__value)

    def __format__(self, format_spec: str):
        return format(self.__value, format_spec)

    def __lt__(self, other: Any):
        return self.__value < other

    def __le__(self, other: Any):
        return self.__value <= other

    def __eq__(self, other: Any):
        return self.__value == other

    def __ne__(self, other: Any):
        return self.__value != other

    def __gt__(self, other: Any):
        return self.__value > other

    def __ge__(self, other: Any):
        return self.__value >= other

    def __hash__(self):
        return hash(self.__value)

    def __bool__(self):
        return bool(self.__value)

    # customizing attribute access

    def __getattr__(self, name: str):
        if name == 'value':
            return self.__value
        return getattr(self.__value, name)

    def __setattr__(self, name: str, value: Any):
        value = unref(value)
        if name.startswith(f'_{self.__class__.__name__}__'):
            super().__setattr__(name, value)
            return
        old_value = self.__value
        if name == 'value':
            if value == self.__value:
                return
            self.__value = value
        else:
            if hasattr(self.__value, name):
                if getattr(self.__value, name) == value:
                    return
            setattr(self.__value, name, value)
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)

    def set_value_without_triggering_change_handlers(self, value: Any):
        value = unref(value)
        old_value = self.__value
        self.__value = value
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)

    def __delattr__(self, name: str):
        if name.startswith('__ProxyValue_'):
            raise AttributeError(name)
        old_value = self.__value
        delattr(self.__value, name)
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)

    def __dir__(self):
        return dir(self.__value)

    # emulating callable objects

    def __call__(self, *args, **kwargs):
        return self.__value(*args, **kwargs)

    # emulating container types

    def __len__(self):
        return len(self.__value)

    def __getitem__(self, key: Any):
        return self.__value[key]

    def __setitem__(self, key: Any, value: Any):
        value = unref(value)
        old_value = self.__value
        self.__value[key] = value
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)

    def __delitem__(self, key: Any):
        old_value = self.__value
        del self.__value[key]
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)

    def __missing__(self, key: Any):
        return self.__value.__missing__(key)

    def __iter__(self):
        return iter(self.__value)

    def __reversed__(self):
        return reversed(self.__value)

    def __contains__(self, item: Any):
        return item in self.__value

    # emulating numeric types

    def __add__(self, other: Any):
        other = unref(other)
        return self.__value + other

    def __sub__(self, other: Any):
        other = unref(other)
        return self.__value - other

    def __mul__(self, other: Any):
        other = unref(other)
        return self.__value * other

    def __truediv__(self, other: Any):
        other = unref(other)
        return self.__value / other

    def __floordiv__(self, other: Any):
        other = unref(other)
        return self.__value // other

    def __mod__(self, other: Any):
        other = unref(other)
        return self.__value % other

    def __divmod__(self, other: Any):
        other = unref(other)
        return divmod(self.__value, other)

    def __pow__(self, other: Any):
        other = unref(other)
        return pow(self.__value, other)

    def __lshift__(self, other: Any):
        other = unref(other)
        return self.__value << other

    def __rshift__(self, other: Any):
        other = unref(other)
        return self.__value >> other

    def __and__(self, other: Any):
        other = unref(other)
        return self.__value & other

    def __xor__(self, other: Any):
        other = unref(other)
        return self.__value ^ other

    def __or__(self, other: Any):
        other = unref(other)
        return self.__value | other

    def __radd__(self, other: Any):
        other = unref(other)
        return other + self.__value

    def __rsub__(self, other: Any):
        other = unref(other)
        return other - self.__value

    def __rmul__(self, other: Any):
        other = unref(other)
        return other * self.__value

    def __rtruediv__(self, other: Any):
        other = unref(other)
        return other / self.__value

    def __rfloordiv__(self, other: Any):
        other = unref(other)
        return other // self.__value

    def __rmod__(self, other: Any):
        other = unref(other)
        return other % self.__value

    def __rdivmod__(self, other: Any):
        other = unref(other)
        return divmod(other, self.__value)

    def __rpow__(self, other: Any):
        other = unref(other)
        return pow(other, self.__value)

    def __rlshift__(self, other: Any):
        other = unref(other)
        return other << self.__value

    def __rrshift__(self, other: Any):
        other = unref(other)
        return other >> self.__value

    def __rand__(self, other: Any):
        other = unref(other)
        return other & self.__value

    def __rxor__(self, other: Any):
        other = unref(other)
        return other ^ self.__value

    def __ror__(self, other: Any):
        other = unref(other)
        return other | self.__value

    def __iadd__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value += other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __isub__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value -= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __imul__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value *= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __itruediv__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value /= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __ifloordiv__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value //= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __imod__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value %= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __ipow__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value **= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __ilshift__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value <<= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __irshift__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value >>= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __iand__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value &= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __ixor__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value ^= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __ior__(self, other: Any):
        other = unref(other)
        old_value = self.__value
        self.__value |= other
        new_value = self.__value
        self.__invoke_change_handlers(new_value, old_value)
        return self

    def __neg__(self):
        return -self.__value

    def __pos__(self):
        return +self.__value

    def __abs__(self):
        return abs(self.__value)

    def __invert__(self):
        return ~self.__value

    def __complex__(self):
        return complex(self.__value)

    def __int__(self):
        return int(self.__value)

    def __float__(self):
        return float(self.__value)

    def __index__(self):
        return self.__value.__index__()

    def __round__(self, n: int = 0):
        return round(self.__value, n)

    def __trunc__(self):
        return self.__value.__trunc__()

    def __floor__(self):
        return self.__value.__floor__()

    def __ceil__(self):
        return self.__value.__ceil__()

    # emulating with statement context managers

    def __enter__(self):
        return self.__value.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.__value.__exit__(exc_type, exc_value, traceback)

    def __await__(self):
        return self.__value.__await__()

    def __aiter__(self):
        return self.__value.__aiter__()

    def __anext__(self):
        return self.__value.__anext__()

    def __aenter__(self):
        return self.__value.__aenter__()

    def __aexit__(self, exc_type, exc_value, traceback):
        return self.__value.__aexit__(exc_type, exc_value, traceback)
