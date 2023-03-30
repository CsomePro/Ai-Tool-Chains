
from __future__ import annotations

class Info:
    name = ''

    @classmethod
    def get_info(cls) -> list:
        pass

class InfoManager:
    local_info_map = {}

    @classmethod
    def register(cls, info: Info):
        assert info.name not in cls.local_info_map
        cls.local_info_map[info.name] = info

    @classmethod
    def get(cls, name: str) -> Info:
        return cls.local_info_map.get(name, None)

