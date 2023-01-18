from typing import Any

from jianmu.pyvar.AbstractRef import AbstractRef


def unref(value: Any):
    if isinstance(value, AbstractRef):
        return unref(value.true_value)
    elif value.__class__.__name__ == 'Proxy':
        return unref(value.value)
    elif isinstance(value, list):
        return [unref(item) for item in value]
    elif isinstance(value, tuple):
        return tuple(unref(item) for item in value)
    elif isinstance(value, set):
        return {unref(item) for item in value}
    elif isinstance(value, dict):
        return {key: unref(item) for key, item in value.items()}
    else:
        return value
