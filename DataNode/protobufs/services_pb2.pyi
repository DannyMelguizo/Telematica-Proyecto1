from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetBlock(_message.Message):
    __slots__ = ("ip", "file", "block")
    IP_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    ip: str
    file: str
    block: int
    def __init__(self, ip: _Optional[str] = ..., file: _Optional[str] = ..., block: _Optional[int] = ...) -> None: ...

class GetBlockResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
