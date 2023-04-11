from __future__ import annotations

from typing import Dict, Optional, Tuple, Any
from uuid import UUID, uuid3
from pydantic import BaseModel, PrivateAttr
from toolchains.myType.base import TypeManager
from toolchains.error.base import *

TOOL_NAMESPACE = UUID("185db940-446b-45fc-87c6-513bb8d8cfea")


def get_tool_uuid_by_name(name: str):
    return str(uuid3(TOOL_NAMESPACE, name))


class ToolsManager:
    local_tools_map = {}

    @classmethod
    def get(cls, uuid) -> ToolFactory:
        return cls.local_tools_map.get(uuid, None)

    @classmethod
    def register(cls, tool: ToolFactory):
        assert tool.get('uuid') not in cls.local_tools_map, f"Duplicate uuid : {tool.get('uuid')}"
        cls.local_tools_map[tool.get('uuid')] = tool
        return tool


class ToolModel(BaseModel):
    uuid: str  # unique tools id
    name: str  # tool's name for human
    desc: str
    nfm: str  # name for model
    dfm: str  # description for model
    # tool's description, try to make clear to AI (just like human learning the tool with dec)
    tag: dict[str, str]  # (export args name[need to be set by user])
    param: dict[str, str] = {}  # store all args
    in_vars: list[str]  # function input variable tag
    out_vars: list[str]  # function output variable tag
    out_map: Optional[Dict[str, Tuple[str, str]]] = {}  # function output variable map
    child: Dict[str, Dict] = {}  # content child tool's args {uuid: child args}
    _args: dict[str, Any] = PrivateAttr({})
    """
    {
        ”uuid“: {
            "uuid": str
            "args": {
                "key": value | "args/key"   
                },
            "next": ["uuid", "uuid"],
            "map": {
                    "var"(in_vars): (uuid | "cur", var)
                }
            }
    }
    """

    def set(self, **kwargs):
        self._args.update(self.param)
        for k, v in self.tag.items():
            arg = kwargs.get(k, None)
            if not TypeManager.get(v).check(arg):
                raise TypeCheckError(f"Type name: {TypeManager.get(v).name}, recv {arg}")
            self._args[k] = arg
        self.config()
        return self

    def compile(self):
        pass

    def config(self):
        pass

    def func(self, **kwargs):
        pass


class ToolFactory:
    tool: ToolModel

    @classmethod
    def new(cls, **kwargs) -> ToolModel:
        return cls.tool.__class__(**cls.tool.dict()).set(**kwargs)

    @classmethod
    def get(cls, name):
        return cls.tool.dict().get(name, None)


class TaskToolModel(ToolModel):
    def topo_base(self, v, visited, stack):
        visited[v] = True
        for to in self.child[v]['next']:
            if not visited[to]:
                self.topo_base(to, visited, stack)
        stack.append(v)

    def topo(self):
        visited = {k: False for k in self.child.keys()}
        stack = []
        for to in self.child.keys():
            if not visited[to]:
                self.topo_base(to, visited, stack)
        stack.reverse()
        return stack

    def get_args_key(self, s: str):
        arr = list(filter(lambda x: x, s.strip().split('/')))
        assert arr[0] == 'args' and len(arr) == 2
        return self._args.get(arr[1], None)

    def func(self, **kwargs):
        for k, v in self.child.items():
            for key, value in v['args'].items():
                if 'args' in value:
                    v['args'][key] = self.get_args_key(value)
        # supports "args/key"
        tool_cache: Dict[str, ToolModel] = {uuid: ToolsManager.get(v.get('uuid')).new(**v.get('args')) for uuid, v
                                            in self.child.items()}
        queue = self.topo()
        var_cache = {"cur": kwargs}

        for uuid in queue:
            input_var = {k: var_cache[v[0]][v[1]] for k, v in self.child[uuid]['map'].items()}
            var_cache[uuid] = tool_cache[uuid].func(**input_var)

        return {k: var_cache[v[0]][v[1]] for k, v in self.out_map.items()}


class SingleInOutToolModel(ToolModel):
    in_vars: list[str] = ['in']
    out_vars: list[str] = ['out']
