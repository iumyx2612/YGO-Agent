from typing import Optional, List, Any, Dict
from typing_extensions import Self
from enum import Enum

from llama_index.core.llms import LLM
from llama_index.core.prompts import ChatMessage

from src.modules.schema.card import CardInfo, CardType
from src.modules.schema.entity.card import Race, Attribute
from src.modules.prompt.analyze.monster.card import (
    MONSTER_PROPERTIES_SYSTEM,
    MONSTER_PROPERTIES_SYSTEM_EXAMPLE,
    MONSTER_PROPERTIES_USER
)
from src.pipelines.card.base_card import BaseCardPipeline


class MonsterPropertiesPipeline(BaseCardPipeline):
    def __init__(self,
                 *args,
                 entity_restrictions: Optional[List[Enum]] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.entity_restrictions = entity_restrictions
        print(self.llm)

    @classmethod
    def from_defaults(cls,
                      llm: LLM,
                      system_prompt: str = MONSTER_PROPERTIES_SYSTEM,
                      user_prompt: str = MONSTER_PROPERTIES_USER,
                      entity_restrictions: List[Enum] = [
                          Race, Attribute
                      ]) -> Self:
        return cls(llm, system_prompt, user_prompt, entity_restrictions=entity_restrictions)

    def schema_to_prompt_kwargs(self) -> Dict[str, str]:
        entity_restriction_str = ""

        for entity_restriction in self.entity_restrictions:
            entity_restriction_str += f"- {entity_restriction.__name__}: {[e.value for e in entity_restriction]}\n\t"

        return {
            "card_type_restriction": f"{[e.value for e in CardType]}",
            "entity_restriction": entity_restriction_str,
            "example": MONSTER_PROPERTIES_SYSTEM_EXAMPLE
        }

    def analyze_card(self,
                     card: CardInfo,
                     pipeline: Optional[BaseCardPipeline] = None,
                     **kwargs) -> str:
        system_prompt_kwargs = self.schema_to_prompt_kwargs()

        system_prompt = self.system_prompt.format(**system_prompt_kwargs)
        user_prompt = self.user_prompt.format(
            info=card.dict()
        )

        messages = [
            ChatMessage(
                content=system_prompt,
                role="system"
            ),
            ChatMessage(
                content=user_prompt,
                role="user"
            )
        ]

        response = self.llm.chat(messages)
        response = response.message.content

        return response

    async def aanalyze_card(self,
                            card: CardInfo,
                            pipeline: Optional[Self] = None,
                            **kwargs) -> str:
        system_prompt_kwargs = self.schema_to_prompt_kwargs()

        system_prompt = self.system_prompt.format(**system_prompt_kwargs)
        user_prompt = self.user_prompt.format(
            info=card.dict()
        )

        messages = [
            ChatMessage(
                content=system_prompt,
                role="system"
            ),
            ChatMessage(
                content=user_prompt,
                role="user"
            )
        ]

        response = await self.llm.achat(messages)
        response = response.message.content

        return response