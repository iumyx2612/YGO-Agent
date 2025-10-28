from typing import Optional, List, Any, Dict
from typing_extensions import Self
from enum import Enum

from llama_index.core.llms import LLM
from llama_index.core.prompts import ChatMessage

from src.modules.schema.type import BaseComponent
from src.modules.schema.card import CardInfo, CardType
from src.modules.schema.entity.card import Race, Attribute
from src.modules.schema.entity.zone import ZoneEntity
from src.modules.schema.entity.summon import SummonMethodEntity
from src.modules.schema.entity.entity import Entities
from src.modules.schema.relation.summon import SummonZoneRelation
from src.modules.prompt.analyze.monster.card import (
    MONSTER_PROPERTIES_SYSTEM,
    MONSTER_PROPERTIES_SYSTEM_EXAMPLE,
    MONSTER_PROPERTIES_USER
)
from src.modules.prompt.analyze.monster.summon import (
    MONSTER_SUMMON_EFFECT_EXTRACTION_SYSTEM,
    MONSTER_SUMMON_EFFECT_EXTRACTION_USER,
    MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_SYSTEM,
    MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_SYSTEM_EXAMPLE,
    MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_USER,
    MONSTER_SUMMON_EFFECT_ANALYZE_SYSTEM,
    MONSTER_SUMMON_EFFECT_ANALYZE_SYSTEM_EXAMPLE,
    MONSTER_SUMMON_EFFECT_ANALYZE_USER
)
from .base_card import BaseCardPipeline


class MonsterCardPipeline(BaseCardPipeline):
    def __init__(self,
                 llm: LLM,
                 system_prompt: str,
                 user_prompt: str,
                 schema: Optional[BaseComponent] = None,
                 **kwargs):
        super().__init__(llm, schema, **kwargs)
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def schema_to_prompt_kwargs(self) -> dict:
        pass

    def analyze_card(self, card: CardInfo, pipeline: Optional[Self], **kwargs) -> Any:
        pass


class MonsterPropertiesPipeline(MonsterCardPipeline):
    def __init__(self,
                 *args,
                 entity_restrictions: Optional[List[Enum]] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.entity_restrictions = entity_restrictions

    @classmethod
    def from_defaults(cls,
                      llm: LLM,
                      system_prompt: str = MONSTER_PROPERTIES_SYSTEM,
                      user_prompt: str = MONSTER_PROPERTIES_USER,
                      entity_restrictions: List[Enum] = [
                          Race, Attribute, CardType
                      ]) -> Self:
        return cls(llm, system_prompt, user_prompt, entity_restrictions=entity_restrictions)

    def schema_to_prompt_kwargs(self) -> Dict[str, str]:
        entity_restriction_str = ""

        for entity_restriction in self.entity_restrictions:
            entity_restriction_str += f"- {entity_restriction.__name__}: {[e.value for e in entity_restriction]}\n\t"

        return {
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

class SummonEffectExtractionMonsterCardPipeline(MonsterCardPipeline):

    @classmethod
    def from_defaults(cls,
                      llm: LLM,
                      system_prompt: str = MONSTER_SUMMON_EFFECT_EXTRACTION_SYSTEM,
                      user_prompt: str = MONSTER_SUMMON_EFFECT_EXTRACTION_USER) -> Self:
        return cls(llm, system_prompt, user_prompt)

    def analyze_card(self, card: CardInfo, pipeline: Optional[BaseCardPipeline] = None, **kwargs) -> str:
        system_prompt = self.system_prompt
        user_prompt = self.user_prompt.format(
            description=card.desc
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


class SummonEffectEntityMonsterCardPipeline(MonsterCardPipeline):
    def __init__(self,
                 llm: LLM,
                 system_prompt: str,
                 user_prompt: str,
                 schema: Optional[BaseComponent] = None,
                 entity_restrictions: Optional[List[Enum]] = None,
                 **kwargs):
        super().__init__(llm, system_prompt, user_prompt, schema)
        self.entity_restrictions = entity_restrictions

    @classmethod
    def from_defaults(cls,
                      llm: LLM,
                      system_prompt: str = MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_SYSTEM,
                      user_prompt: str = MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_USER,
                      schema: BaseComponent = Entities,
                      entity_restrictions: List[Enum] = [
                          ZoneEntity, SummonMethodEntity
                      ]) -> Self:
        return cls(llm, system_prompt, user_prompt, schema,
                   entity_restrictions=entity_restrictions)

    def schema_to_prompt_kwargs(self) -> Dict[str, str]:
        entity_restriction_str = ""

        for entity_restriction in self.entity_restrictions:
            entity_restriction_str += f"- {entity_restriction.__name__}: {[e.value for e in entity_restriction]}\n\t"

        return {
            "schema": self.schema.model_json_schema(),
            "entity_restriction": entity_restriction_str,
            "example": MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_SYSTEM_EXAMPLE
        }

    def analyze_card(self,
                     card: CardInfo,
                     effect: str,
                     pipeline: Optional[BaseCardPipeline] = None,
                     **kwargs) -> str:
        system_prompt_kwargs = self.schema_to_prompt_kwargs()

        system_prompt = self.system_prompt.format(**system_prompt_kwargs)
        user_prompt = self.user_prompt.format(
            effect=effect
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