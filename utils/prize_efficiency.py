from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from factory.deck_scorer_state import CardState


def prize_efficiency(deck: List[CardState], ct: dict) -> float:
    try:
        atk = ct.get("attackers", [])
        pe = min(1.0, sum(a.damage_output / max(1, a.energy_cost) for a in atk) / len(atk) / 100) if atk else 0.0
        
        req = {c.element_type for c in deck if c.card_type == "Pokemon"}
        req.discard("")
        
        mm = sum(0.02 for e in deck if e.card_type == "Energy" and "basic" in e.card_name.lower()
                 and not any(r.lower() in e.card_name.lower() for r in req) and req)
                 
        pe = max(0.0, pe - mm)
        
        # Tool and Stadium generic synergy logic (from Kaggle analytics)
        tools_count = sum(1 for c in deck if "tool" in c.combo_tags or "tool" in c.card_name.lower())
        stadiums_count = sum(1 for c in deck if "stadium" in c.combo_tags or "stadium" in c.card_name.lower())
        
        # Balance bonus for utilizing tools and stadiums appropriately
        if 1 <= tools_count <= 4:
            pe += 0.05
        if 1 <= stadiums_count <= 4:
            pe += 0.05
            
        return min(1.0, pe)
    except Exception as e:
        return 0.0

