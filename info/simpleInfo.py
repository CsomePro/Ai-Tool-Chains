from toolchains.info.base import *
from toolchains.tool import ToolsManager
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
                'dec': v.get('dec'),
                'tag': {_k: TypeManager.get(_v).get() for _k, _v in v.get('tag').items()},
                'in_vars': v.get('in_vars'),
                'out_vars': v.get('out_vars'),
            } for k, v in ToolsManager.local_tools_map.items()]
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
                'dec': v.get('dec'),
                'in_vars': v.get('in_vars'),
                'out_vars': v.get('out_vars'),
                'tag': {_k: TypeManager.get(_v).get() for _k, _v in v.get('tag').items()}
            } for k, v in AgentsManager.local_agents_map.items()]
        print(data)
        return data
