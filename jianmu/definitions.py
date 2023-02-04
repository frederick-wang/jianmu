from dataclasses import dataclass


@dataclass
class File:
    lastModified: int
    name: str
    bytes: bytes
    path: str
    size: int
    type: str
    webkitRelativePath: str


