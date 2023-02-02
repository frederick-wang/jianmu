from typing import Any, Callable, List, Optional
from typing_extensions import NotRequired, TypedDict
from .sock import get_socketio


class FileFilter(TypedDict):
    name: str
    extensions: List[str]


class ShowSaveDialogOptions(TypedDict):
    defaultPath: NotRequired[str]
    buttonLabel: NotRequired[str]
    filters: NotRequired[List[FileFilter]]


class ShowSaveDialogResult(TypedDict):
    filePath: str
    canceled: bool


def show_save_dialog(
    options: Optional[ShowSaveDialogOptions] = None,
    callback: Optional[Callable[[ShowSaveDialogResult], None]] = None,
) -> None:
    if options is None:
        options = {}
    if callback is None:
        callback = lambda result: None
    socketio = get_socketio()
    socketio.emit('Action:show-save-dialog', options, callback=callback)
