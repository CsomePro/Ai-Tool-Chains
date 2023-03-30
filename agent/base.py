from __future__ import annotations

from pydantic import PrivateAttr

from uuid import UUID, uuid3

from toolchains.llm.base import LLmManager
import langchain

from toolchains.tool import ToolsManager, SingleInOutToolModel
from toolchains.myType.simpleType import LLmUUIDType, ListToolType, AgentType

AGENT_NAMESPACE = UUID("185db942-446b-45fc-87c6-513bb8d8cfea")


def get_agent_uuid_by_name(name: str):
    return str(uuid3(AGENT_NAMESPACE, name))


class AgentsManager:
    local_agents_map = {}

    @classmethod
    def get(cls, uuid) -> AgentModel:
        return cls.local_agents_map.get(uuid, None)

    @classmethod
    def register(cls, agent: AgentFactory):
        assert agent.get('uuid') not in cls.local_agents_map, f"Duplicate agent uuid : {agent.get('uuid')}"
        cls.local_agents_map[agent.get('uuid')] = agent
        return agent


class AgentModel(SingleInOutToolModel):
    tag: dict[str, str] = {'llm_uuid': LLmUUIDType.uuid,
                           'tools': ListToolType.uuid,
                           'agent': AgentType.uuid}
    _agent = PrivateAttr()


class TaskAgentModel(AgentModel):
    _is_config: bool = PrivateAttr(False)

    def config(self):
        llm_uuid = self._args['llm_uuid']
        llm = LLmManager.get(llm_uuid).new(**self.child.get(llm_uuid, {}))
        raw_tools = [ToolsManager.get(uuid).new(**self.child.get(uuid, {})) for uuid in self._args['tools']]
        tools = []
        for tool in raw_tools:
            assert len(tool.in_vars) == 1 and len(tool.out_vars), f"The number of tool ({tool.name}) input " \
                                                                  f"and output variable should be only one "
            tools.append(langchain.agents.Tool(
                name=tool.name,
                description=tool.dec,
                func=lambda x: tool.func(**{tool.in_vars[0]: x})[tool.out_vars[0]]
            ))
        self._agent = langchain.agents.initialize_agent(tools, llm.get_llm(), agent=self._args['agent'], verbose=True)
        self._is_config = True

    def func(self, **kwargs):
        return {
            self.out_vars[0]: self._agent.run(kwargs[self.in_vars[0]])
        }


class AgentFactory:
    agent: AgentModel

    @classmethod
    def new(cls, **kwargs) -> AgentModel:
        return cls.agent.__class__(**cls.agent.dict()).set(**kwargs)

    @classmethod
    def get(cls, name):
        return cls.agent.dict().get(name, None)
