from __future__ import annotations

from abc import ABC,abstractmethod
from typing import ClassVar
from uuid import UUID, uuid3
from pydantic import BaseModel

TYPE_NAMESPACE = UUID("185db944-446b-45fc-87c6-513bb8d8cfea")

def get_type_uuid_by_name(name: str):
    return str(uuid3(TYPE_NAMESPACE, name))

class Type(BaseModel):
    uuid: ClassVar[str]
    name: ClassVar[str]
    dec: ClassVar[str]

    @classmethod
    def check(cls, var: object) -> bool:
        pass

    @classmethod
    def get(cls):
        pass

class TypeManager:
    local_type_map: dict[str, Type] = {}

    @classmethod
    def get(cls, uuid) -> Type:
        return cls.local_type_map.get(uuid, None)

    @classmethod
    def register(cls, t: Type):
        assert t.uuid not in cls.local_type_map, f"Duplication uuid Type {t.uuid}"
        cls.local_type_map[t.uuid] = t
        return t
