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
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, nodes: _Optional[_Iterable[str]] = ...) -> None: ...

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
