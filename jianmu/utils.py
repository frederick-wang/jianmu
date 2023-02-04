import base64
from io import BytesIO
import os
from typing import Any


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def datauri_to_bytes(s: str) -> bytes:
    # sourcery skip: assign-if-exp, reintroduce-else
    lst = s.split(',')
    if len(lst) == 1:
        return base64.b64decode(lst[0])
    return base64.b64decode(lst[1])


def base64_to_bytes(s: str) -> bytes:
    return base64.b64decode(s)


try:
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt

    def figure_to_datauri(fig: Figure, **kwargs: Any) -> str:  # type: ignore
        format_arg = kwargs.get('format', 'png')
        with BytesIO() as fig_bytes:
            fig.savefig(fig_bytes, format=format_arg, **kwargs)
            fig_bytes.seek(0)
            datauri = 'data:image/png;base64,' + base64.b64encode(fig_bytes.read()).decode('utf-8')
            plt.close(fig)
        return datauri
except ImportError:

    def figure_to_datauri(fig: Any, **kwargs: Any) -> str:
        raise ImportError('matplotlib is not installed')
