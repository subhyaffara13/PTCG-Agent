from typing import Set, List, Dict
from dataclasses import dataclass, field

@dataclass
class CardState:
    card_id: str
    card_name: str
    card_type: str
    stage: str
    previous_stage: str
    energy_cost: int
    damage_output: int
    element_type: str
    combo_tags: Set[str] = field(default_factory=set)

    @classmethod
    def from_dict(cls, c: dict, details: dict) -> 'CardState':
        card_id = str(c.get("card_id", ""))
        det = details.get(card_id, {})
        tags_raw = c.get("combo_tags", [])
        if isinstance(tags_raw, str):
            tags = {tags_raw.lower()}
        else:
            tags = {str(t).lower() for t in tags_raw}
        return cls(
            card_id=card_id,
            card_name=c.get("card_name", "").lower(),
            card_type=c.get("card_type", ""),
            stage=det.get("stage", ""),
            previous_stage=str(det.get("previous_stage") or "").lower(),
            energy_cost=c.get("energy_cost", 0),
            damage_output=c.get("damage_output", 0),
            element_type=det.get("element_type", ""),
            combo_tags=tags
        )
