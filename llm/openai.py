from toolchains.llm.base import LLmFactory, LLmModel, LLmManager, get_llm_uuid_by_name
from langchain.llms import OpenAI
from toolchains.myType.simpleType import FloatType

@LLmManager.register
class OpenaiLLm(LLmFactory):
    class _llm(LLmModel):
        def config(self):
            self._llm = OpenAI(temperature=self._args['temperature'])
    llm = _llm(
        uuid=get_llm_uuid_by_name(locals()['__qualname__']),
        tag={'temperature': FloatType.uuid},
        name='OpenAi GPT Chat',
        dec='LLM Large Language Model from Openai')


