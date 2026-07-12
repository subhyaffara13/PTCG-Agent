"""
cb_agents/card_entry.py

Defines the CardEntry dataclass used for representing card metadata and scoring data.
"""

from dataclasses import dataclass
from cb_agents.card_types import CardType, CardStage, TrainerSubtype, ComboTag

@dataclass(frozen=True)
class CardEntry:
    card_id: int
    card_name: str
    card_type: CardType
    stage: CardStage
    trainer_subtype: TrainerSubtype = TrainerSubtype.NONE
    combo_tags: ComboTag = ComboTag.NONE
    ev_score: float = 0.0
    damage_output: int = 0
    energy_cost: int = 0
    utility_score: float = 0.0
    archetype: str = ""
    previous_stage: str = ""
    hp: int = 100
    retreat_cost: int = 1
    is_full: bool = False
