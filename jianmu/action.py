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
    filePaths: List[str]
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


def show_open_dialog(options: Optional[OpenDialogOptions] = None) -> OpenDialogReturnValue:
    if options is None:
        options = {}
    return_value: Optional[OpenDialogReturnValue] = None

    def callback(result: OpenDialogReturnValue) -> None:
        nonlocal return_value
        return_value = result

    socketio = get_socketio()
    socketio.emit('Action:show-open-dialog', {'args': [options]}, callback=callback)

    while True:
        if return_value is not None:
            return return_value
        socketio.sleep(0.05)  # type: ignore


def show_save_dialog(options: Optional[SaveDialogOptions] = None) -> SaveDialogReturnValue:
    if options is None:
        options = {}
    return_value: Optional[SaveDialogReturnValue] = None

    def callback(result: SaveDialogReturnValue) -> None:
        nonlocal return_value
        return_value = result

    socketio = get_socketio()
    socketio.emit('Action:show-save-dialog', {'args': [options]}, callback=callback)

    while True:
        if return_value is not None:
            return return_value
        socketio.sleep(0.05)  # type: ignore


def show_message_box(options: MessageBoxOptions) -> MessageBoxReturnValue:
    return_value: Optional[MessageBoxReturnValue] = None

    def callback(result: MessageBoxReturnValue) -> None:
        nonlocal return_value
        return_value = result

    socketio = get_socketio()
    socketio.emit('Action:show-message-box', {'args': [options]}, callback=callback)

    while True:
        if return_value is not None:
            return return_value
        socketio.sleep(0.05)  # type: ignore


def show_error_box(title: str, content: str) -> None:
    can_be_returned = False

    def callback(result: None) -> None:
        nonlocal can_be_returned
        can_be_returned = True

    socketio = get_socketio()
    socketio.emit('Action:show-error-box', {'args': [title, content]}, callback=callback)

    while True:
        if can_be_returned:
            return None
        socketio.sleep(0.05)  # type: ignore


def show_item_in_folder(full_path: str) -> None:
    can_be_returned = False

    def callback(result: None) -> None:
        nonlocal can_be_returned
        can_be_returned = True

    socketio = get_socketio()
    socketio.emit('Action:show-item-in-folder', {'args': [full_path]}, callback=callback)

    while True:
        if can_be_returned:
            return None
        socketio.sleep(0.05)  # type: ignore


def open_path(path: str) -> str:
    return_value: Optional[str] = None

    def callback(result: str) -> None:
        nonlocal return_value
        return_value = result

    socketio = get_socketio()
    socketio.emit('Action:open-path', {'args': [path]}, callback=callback)

    while True:
        if return_value is not None:
            return return_value
        socketio.sleep(0.05)  # type: ignore


def open_external(url: str, options: Optional[OpenExternalOptions] = None) -> None:
    if options is None:
        options = {}
    can_be_returned = False

    def callback(result: None) -> None:
        nonlocal can_be_returned
        can_be_returned = True

    socketio = get_socketio()
    socketio.emit('Action:open-external', {'args': [url, options]}, callback=callback)

    while True:
        if can_be_returned:
            return None
        socketio.sleep(0.05)  # type: ignore


def trash_item(path: str) -> None:
    can_be_returned = False

    def callback(result: None) -> None:
        nonlocal can_be_returned
        can_be_returned = True

    socketio = get_socketio()
    socketio.emit('Action:trash-item', {'args': [path]}, callback=callback)

    while True:
        if can_be_returned:
            return None
        socketio.sleep(0.05)  # type: ignore


def beep() -> None:
    can_be_returned = False

    def callback(result: None) -> None:
        nonlocal can_be_returned
        can_be_returned = True

    socketio = get_socketio()
    socketio.emit('Action:beep', {'args': []}, callback=callback)

    while True:
        if can_be_returned:
            return None
        socketio.sleep(0.05)  # type: ignore
