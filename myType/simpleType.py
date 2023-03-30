from toolchains.myType.base import Type, TypeManager, get_type_uuid_by_name
import toolchains.myType.config as config
from toolchains.llm.base import LLmManager
from toolchains.tool import ToolsManager


@TypeManager.register
class IntType(Type):
    name = locals()['__qualname__']
    uuid = get_type_uuid_by_name(name)
    dec = config.TYPE.INT

    @classmethod
    def check(cls, var: int) -> bool:
        if not isinstance(var, str):
            return False
        return True


@TypeManager.register
class FloatType(Type):
    name = locals()['__qualname__']
    uuid = get_type_uuid_by_name(name)
    dec = config.TYPE.FLOAT

    @classmethod
    def check(cls, var: float) -> bool:
        if not isinstance(var, float) and not isinstance(var, int):
            return False
        return True


@TypeManager.register
class AgentType(Type):
    name = locals()['__qualname__']
    uuid = get_type_uuid_by_name(name)
    dec = config.TYPE.STRING
    _have = {
        'zero-shot-react-description',
        "react-docstore",
        "self-ask-with-search",
        "conversational-react-description",
    }

    @classmethod
    def check(cls, var: int) -> bool:
        if not isinstance(var, str):
            return False
        if var not in cls._have:
            return False
        return True

    @classmethod
    def get(cls):
        return {'type': "option", 'value': [
            {'value': _, 'label': _} for _ in cls._have
        ], 'default': 'zero-shot-react-description'}


@TypeManager.register
class ListToolType(Type):
    name = locals()['__qualname__']
    uuid = get_type_uuid_by_name(name)
    dec = config.TYPE.LIST_STR

    @classmethod
    def check(cls, var: list[str]) -> bool:
        if not isinstance(var, list):
            return False
        for t in var:
            if not isinstance(t, str):
                return False
            if t not in ToolsManager.local_tools_map:
                return False
        return True

    @classmethod
    def get(cls):
        return {'type': 'multi', 'value': [
            {'value': v.get('uuid'), 'label': v.get('name'), 'dec': v.get('dec')} for k, v in
            ToolsManager.local_tools_map.items()
        ],
                'default': ''
                }


@TypeManager.register
class LLmUUIDType(Type):
    name = locals()['__qualname__']
    uuid = get_type_uuid_by_name(name)
    dec = config.LLM_UUID_TYPE

    @classmethod
    def check(cls, var: str) -> bool:
        if not isinstance(var, str):
            return False
        if var not in LLmManager.local_llm_map:
            return False
        return True

    @classmethod
    def get(cls):
        return {'type': "option", 'value': [
            {'value': v.get('uuid'), 'label': v.get('name'), 'dec': v.get('dec')} for k, v in
            LLmManager.local_llm_map.items()
        ], 'default': ''}


@TypeManager.register
class RegexType(Type):
    name = locals()['__qualname__']
    uuid = get_type_uuid_by_name(name)
    dec = config.TYPE.STRING

    @classmethod
    def check(cls, var: int) -> bool:
        if not isinstance(var, str):
            return False
        return True

    @classmethod
    def get(cls):
        return {'type': "text", 'default': ''}