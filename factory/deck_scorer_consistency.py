import math
from typing import List
from factory.deck_scorer_state import CardState

def consistency_score(deck: List[CardState], ct: dict) -> float:
    try:
        prob_brick = math.comb(60 - ct.get("basic", 0), 7) / math.comb(60, 7) if ct.get("basic", 0) <= 53 else 0.0
        prob_open = 1.0 - prob_brick
        
        cs = min(1.0, max(0.0, (ct.get("basic", 0) / 60) * (ct.get("sup", 0) / 60) * 2.0))
        if prob_open < 0.85: 
            cs = max(0.0, cs - 0.3)
            
        names = {c.card_name for c in deck}
        evo_pen = sum(0.05 for c in deck if c.card_type == "Pokemon" and c.previous_stage and c.previous_stage not in names)
        
        pyr = (0.15 if ct.get("s1", 0) > 0 and ct.get("basic", 0) <= ct.get("s1", 0) else 0) + \
              (0.15 if ct.get("s2", 0) > 0 and ct.get("s1", 0) <= ct.get("s2", 0) else 0)
        
        cs = max(0.0, cs - evo_pen - pyr)
        if ct.get("item", 0) < ct.get("sup", 0) and ct.get("sup", 0) > 0: 
            cs = max(0.0, cs - 0.1)
            
        atk3 = sum(1 for a in ct.get("attackers", []) if a.energy_cost >= 3)
        accel = sum(1 for c in deck if "attach" in c.combo_tags)
        
        if atk3 > 0 and accel < 2: 
            cs = max(0.0, cs - 0.25)
            
        return cs
    except Exception as e:
        return 0.0

def recovery_score(ct: dict) -> float:
    try:
        rs = min(1.0, ct.get("sup", 0) / 15.0)
        return min(1.0, rs + 0.1) if ct.get("rec", 0) >= 2 else (max(0.0, rs - 0.1) if ct.get("rec", 0) == 0 else rs)
    except Exception:
        return 0.0
