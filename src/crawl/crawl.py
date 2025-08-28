from typing import Optional, Literal

from .const import Race
from .model import CardInfo


def crawl(
        name: Optional[str] = None,
        fname: Optional[str] = None,
        archetype: Optional[str] = None,
        level: Optional[int] = None,
        race: Optional[Race] = None,
        attribute: Optional[Literal[
            "DARK", "DIVINE", "EARTH",
            "FIRE", "LIGHT", "WATER", "WIND"
        ]] = None,
        link: Optional[int] = None
) -> CardInfo:
    parameter_string = "?"
