from toolchains.info.base import *
from toolchains.tool.base import ToolsManager
from toolchains.agent import AgentsManager
from toolchains.myType.simpleType import TypeManager


@InfoManager.register
class ToolsInfo(Info):
    name = "tools_info"

    @classmethod
    def get_info(cls) -> list:
        data = [
            {
                'uuid': k,
                'name': v.get('name'),
                'desc': v.get('desc'),
                'tag': {_k: TypeManager.get(_v).get() for _k, _v in v.get('tag').items()},
                'in_vars': v.get('in_vars'),
                'out_vars': v.get('out_vars'),
            } for k, v in ToolsManager.local_tools_map.items()]
        return data

@InfoManager.register
class SingleToolInfo(Info):
    name = "single_tool_info"

    @classmethod
    def get_info(cls, uuid) -> dict:
        v = ToolsManager.get(uuid)
        data = {
                'uuid': v.get('uuid'),
                'name': v.get('name'),
                'desc': v.get('desc'),
                'tag': {_k: TypeManager.get(_v).get() for _k, _v in v.get('tag').items()},
                'in_vars': v.get('in_vars'),
                'out_vars': v.get('out_vars'),
            }
        return data

@InfoManager.register
class AgentsInfo(Info):
    name = "agents_info"

    @classmethod
    def get_info(cls):
        data = [
            {
                'uuid': k,
                'name': v.get('name'),
                'desc': v.get('desc'),
                'in_vars': v.get('in_vars'),
                'out_vars': v.get('out_vars'),
                'tag': {_k: TypeManager.get(_v).get() for _k, _v in v.get('tag').items()}
            } for k, v in AgentsManager.local_agents_map.items()]
        print(data)
        return data
