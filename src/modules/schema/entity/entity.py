from typing import List
from src.modules.schema.type import BaseComponent


class EntityInfo(BaseComponent):
    entity_name: str
    entity_description: str


class Entities(BaseComponent):
    entities: List[EntityInfo]