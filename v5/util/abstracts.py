from __future__ import annotations
from abc import ABCMeta, abstractmethod
from .type_hints import JSON


class JsonObject(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def fromJson(cls, data: JSON) -> JsonObject:   ...

    @abstractmethod
    def toJson(cls) -> JSON:     ...
