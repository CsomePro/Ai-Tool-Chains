from toolchains.agent.base import *


@AgentsManager.register
class SimpleAgent(AgentFactory):
    agent = TaskAgentModel(uuid=get_agent_uuid_by_name(locals()['__qualname__']),
                 name='Simple Agent', dec='Easy Assistant')
