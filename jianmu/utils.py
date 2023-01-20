import base64
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def base64_src_to_bytes(s: str) -> bytes:
    # sourcery skip: assign-if-exp, reintroduce-else
    lst = s.split(',')
    if len(lst) == 1:
        return base64.b64decode(lst[0])
    return base64.b64decode(lst[1])


def base64_to_bytes(s: str) -> bytes:
    return base64.b64decode(s)
