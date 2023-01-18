import base64

from . import exceptions, info


def base64_to_bytes(s: str) -> bytes:
    # sourcery skip: assign-if-exp, reintroduce-else
    lst = s.split(',')
    if len(lst) == 1:
        return base64.b64decode(lst[0])
    return base64.b64decode(lst[1])


__all__ = ['exceptions', 'info', 'base64_to_bytes']
