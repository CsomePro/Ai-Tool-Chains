from __future__ import annotations

from pydantic import PrivateAttr
from uuid import UUID, uuid3
from langchain.llms import BaseLLM
from toolchains.tool.base import SingleInOutToolModel

LLM_NAMESPACE = UUID("185db941-446b-45fc-87c6-513bb8d8cfea")


def get_llm_uuid_by_name(name: str):
    return str(uuid3(LLM_NAMESPACE, name))


class LLmManager:
    local_llm_map: dict[str, LLmFactory] = {}

    @classmethod
    def get(cls, uuid) -> LLmFactory:
        return cls.local_llm_map.get(uuid, None)

    @classmethod
    def register(cls, llm: LLmFactory):
        assert llm.get('uuid') not in cls.local_llm_map, f"Duplicate agent uuid : {llm.get('uuid')}"
        cls.local_llm_map[llm.get('uuid')] = llm
        return llm


class LLmModel(SingleInOutToolModel):
    _llm: BaseLLM = PrivateAttr()

    def get_llm(self) -> BaseLLM:
        return self._llm

    def func(self, **kwargs):
        return {self.out_vars[0]: self._llm.generate(kwargs.get(self.in_vars[0], ''))}


class LLmFactory:
    llm: LLmModel

    @classmethod
    def new(cls, **kwargs) -> LLmModel:
        return cls.llm.__class__(**cls.llm.dict()).set(**kwargs)

    @classmethod
    def get(cls, name):
        return cls.llm.dict().get(name, None)
