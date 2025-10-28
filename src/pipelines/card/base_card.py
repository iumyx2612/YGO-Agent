from typing import Optional, Any, List
from typing_extensions import Self
from abc import ABC, abstractmethod

from llama_index.core.llms import LLM

from src.modules.schema.type import BaseComponent
from src.modules.schema.card import CardInfo


class BaseCardPipeline(ABC):
    def __init__(self,
                 llm: LLM,
                 system_prompt: str,
                 user_prompt: str,
                 schema: Optional[BaseComponent] = None,
                 **kwargs):
        self.llm = llm
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.schema = schema

    @abstractmethod
    def schema_to_prompt_kwargs(self) -> dict:
        ...

    @abstractmethod
    def analyze_card(self, card: CardInfo, pipeline: Optional[Self] = None, **kwargs) -> str:
        ...

    @abstractmethod
    async def aanalyze_card(self, card: CardInfo, pipeline: Optional[Self] = None, **kwargs) -> str:
        ...