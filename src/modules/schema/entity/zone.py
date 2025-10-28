from enum import Enum


class ZoneEntity(str, Enum):
    Extra_Deck = "Extra"
    Main_Deck = "Main"
    Graveyard = "Graveyard"
    Banishment = "Banishment"
    Monster_Zone = "Monster Zone"
    SpellTrap_Zone = "Spell/Trap Zone"
    Field = "Field"
    Hand = "Hand"