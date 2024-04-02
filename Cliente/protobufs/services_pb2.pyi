from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NameFile(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Nodes(_message.Message):
    __slots__ = ("keys", "values")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    keys: bytes
    values: bytes
    def __init__(self, keys: _Optional[bytes] = ..., values: _Optional[bytes] = ...) -> None: ...

class UploadFile(_message.Message):
    __slots__ = ("name", "size")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    def __init__(self, name: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class NodesToSend(_message.Message):
    __slots__ = ("blocks", "nodes")
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    blocks: int
    nodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, blocks: _Optional[int] = ..., nodes: _Optional[_Iterable[str]] = ...) -> None: ...

class GetFilesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetFilesResponse(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, files: _Optional[_Iterable[str]] = ...) -> None: ...

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
