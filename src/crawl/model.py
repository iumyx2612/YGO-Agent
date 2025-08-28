from typing import Literal, List

from llama_index.core.schema import BaseComponent


class CardImages(BaseComponent):
    id: int
    image_url: str
    image_url_small: str
    image_url_cropped: str


class CardInfo(BaseComponent):
    archetype: str
    atk: int
    attribute: Literal[
        "DARK", "DIVINE", "EARTH",
        "FIRE", "LIGHT", "WATER", "WIND"
    ]
    card_images: List[CardImages]
    _def: int
    desc: str
    level: int
    name: str
    race: str
    type: str
