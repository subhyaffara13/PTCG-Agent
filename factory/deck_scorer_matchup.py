from typing import List
from factory.deck_scorer_state import CardState

def matchup_spread(deck: List[CardState], ct: dict) -> float:
    try:
        ms = 0.8
        
        # Tracking gust capability
        gust = sum(1 for c in deck if "gust" in c.combo_tags or "switch" in c.combo_tags)
        if gust == 0: 
            ms = max(0.0, ms - 0.2)
            
        # Weakness/Resistance generic coverage
        # A good deck has varying types to avoid total weakness countering
        attacker_types = set()
        for c in deck:
            if c.card_type == "Pokemon" and c.energy_cost > 0:
                if c.element_type:
                    attacker_types.add(c.element_type)
        
        # Bonus for having multiple attacking types (handles weakness spread)
        if len(attacker_types) >= 2:
            ms = min(1.0, ms + 0.15)
            
        return ms
    except Exception:
        return 0.0
