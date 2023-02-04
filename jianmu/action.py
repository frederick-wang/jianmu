from typing import Any, Callable, List, Optional
from typing_extensions import NotRequired, TypedDict
from .sock import get_socketio


class FileFilter(TypedDict):
    name: str
    extensions: List[str]


class SaveDialogOptions(TypedDict):
    defaultPath: NotRequired[str]
    buttonLabel: NotRequired[str]
    filters: NotRequired[List[FileFilter]]
    properties: NotRequired[List[str]]


class OpenDialogOptions(TypedDict):
    title: NotRequired[str]
    defaultPath: NotRequired[str]
    buttonLabel: NotRequired[str]
    filters: NotRequired[List[FileFilter]]
    properties: NotRequired[List[str]]


class SaveDialogReturnValue(TypedDict):
    filePath: str
    canceled: bool


class OpenDialogReturnValue(TypedDict):
    filePath: str
    canceled: bool


class MessageBoxOptions(TypedDict):
    message: str
    type: NotRequired[str]
    buttons: NotRequired[List[str]]
    defaultId: NotRequired[int]
    title: NotRequired[str]
    detail: NotRequired[str]
    checkboxLabel: NotRequired[str]
    checkboxChecked: NotRequired[bool]
    icon: NotRequired[str]
    noLink: NotRequired[bool]
    normalizeAccessKeys: NotRequired[bool]


class MessageBoxReturnValue(TypedDict):
    response: int
    checkboxChecked: bool


class OpenExternalOptions(TypedDict):
    activate: NotRequired[bool]
    '''
    `true` to bring the opened application to the foreground. The default is `true`.
    @platform darwin
    '''
    workingDirectory: NotRequired[str]
    '''
    The working directory.
    @platform win32
    '''


def show_open_dialog(
    options: Optional[OpenDialogOptions] = None,
    callback: Optional[Callable[[OpenDialogReturnValue], None]] = None,
) -> None:
    if options is None:
        options = {}
    if callback is None:
        callback = lambda result: None
    socketio = get_socketio()
    socketio.emit('Action:show-open-dialog', {'args': [options]}, callback=callback)


def show_save_dialog(
    options: Optional[SaveDialogOptions] = None,
    callback: Optional[Callable[[SaveDialogReturnValue], None]] = None,
) -> None:
    if options is None:
        options = {}
    if callback is None:
        callback = lambda result: None
    socketio = get_socketio()
    socketio.emit('Action:show-save-dialog', {'args': [options]}, callback=callback)


def show_message_box(
    options: MessageBoxOptions,
    callback: Optional[Callable[[MessageBoxReturnValue], None]] = None,
) -> None:
    if callback is None:
        callback = lambda result: None
    socketio = get_socketio()
    socketio.emit('Action:show-message-box', {'args': [options]}, callback=callback)


def show_error_box(
    title: str,
    content: str,
    callback: Optional[Callable[[], None]] = None,
) -> None:
    if callback is None:
        callback = lambda: None
    socketio = get_socketio()
    socketio.emit('Action:show-error-box', {'args': [title, content]}, callback=callback)


def show_item_in_folder(full_path: str, callback: Optional[Callable[[], None]] = None) -> None:
    if callback is None:
        callback = lambda: None
    socketio = get_socketio()
    socketio.emit('Action:show-item-in-folder', {'args': [full_path]}, callback=callback)


def open_path(path: str, callback: Optional[Callable[[str], None]] = None) -> None:
    if callback is None:
        callback = lambda error_message: None
    socketio = get_socketio()
    socketio.emit('Action:open-path', {'args': [path]}, callback=callback)


def open_external(url: str,
                  options: Optional[OpenExternalOptions] = None,
                  callback: Optional[Callable[[], None]] = None) -> None:
    if options is None:
        options = {}
    if callback is None:
        callback = lambda: None
    socketio = get_socketio()
    socketio.emit('Action:open-external', {'args': [url, options]}, callback=callback)


def trash_item(path: str, callback: Optional[Callable[[], None]] = None) -> None:
    if callback is None:
        callback = lambda: None
    socketio = get_socketio()
    socketio.emit('Action:trash-item', {'args': [path]}, callback=callback)


def beep(callback: Optional[Callable[[], None]] = None) -> None:
    if callback is None:
        callback = lambda: None
    socketio = get_socketio()
    socketio.emit('Action:beep', {'args': []}, callback=callback)
