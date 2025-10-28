from typing import Literal, List, Optional, Any, Dict
from enum import Enum

from llama_index.core.bridge.pydantic import Field, SerializeAsAny

from src.modules.schema.entity.card import Race
from .type import BaseComponent, EntityNode


class CardType(str, Enum):
    Effect_Monster = "Effect Monster"
    Normal_Monster = "Normal Monster"
    Spell = "Spell"
    Trap = "Trap"
    Link = "Link"
    Synchron = "Synchron"
    Fusion = "Fusion"


class CardRequest(BaseComponent):
    name: Optional[str] = None
    fname: Optional[str] = None
    archetype: Optional[str] = None
    level: Optional[int] = None
    race: Optional[Race] = None
    attribute: Optional[Literal[
        "DARK", "DIVINE", "EARTH",
        "FIRE", "LIGHT", "WATER", "WIND"
    ]] = None
    link: Optional[int] = None


class CardImages(BaseComponent):
    id: int
    image_url: str
    image_url_small: str
    image_url_cropped: str


class CardInfo(BaseComponent):
    desc: str
    name: str
    type: str
    card_images: List[CardImages]
    archetype: Optional[str] = None
    atk: Optional[int] = None
    attribute: Optional[Literal[
        "DARK", "DIVINE", "EARTH",
        "FIRE", "LIGHT", "WATER", "WIND"
    ]] = None
    _def: Optional[int] = None
    level: Optional[int] = None
    race: Optional[str] = None


class CardNode(EntityNode):
    name: str = Field(
        default="",
        description="Card name"
    )
    label: CardType = Field(
        default="",
        description="Card type"
    )
    info: CardInfo
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A flat dictionary of metadata fields",
        alias="extra_info",
    )