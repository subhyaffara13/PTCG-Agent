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
            
        # Check energy-type compatibility
        # Get all energy types present in the deck
        energies_in_deck = {c.card_name for c in deck if c.card_type == "Energy"}
        # Map energy names to elemental types
        has_fire = any("fire" in e.lower() or "{r}" in e.lower() for e in energies_in_deck)
        has_lightning = any("lightning" in e.lower() or "{l}" in e.lower() for e in energies_in_deck)
        has_grass = any("grass" in e.lower() or "{g}" in e.lower() for e in energies_in_deck)
        has_fighting = any("fighting" in e.lower() or "{f}" in e.lower() for e in energies_in_deck)
        has_water = any("water" in e.lower() or "{w}" in e.lower() for e in energies_in_deck)
        has_psychic = any("psychic" in e.lower() or "{p}" in e.lower() for e in energies_in_deck)
        has_metal = any("metal" in e.lower() or "{m}" in e.lower() for e in energies_in_deck)
        has_dark = any("dark" in e.lower() or "{d}" in e.lower() for e in energies_in_deck)

        # Check if any Pokemon has an energy cost but NO matching energy type in deck
        mismatched_pokemon = 0
        for c in deck:
            if c.card_type == "Pokemon" and c.energy_cost > 0:
                elem = (c.element_type or c.card_name).lower()
                needs_grass = "grass" in elem or "{g}" in elem or "ogerpon" in c.card_name
                needs_water = "water" in elem or "{w}" in elem
                needs_psychic = "psychic" in elem or "{p}" in elem
                needs_metal = "metal" in elem or "{m}" in elem
                needs_dark = "dark" in elem or "{d}" in elem

                if (needs_grass and not has_grass) or (needs_water and not has_water) or \
                   (needs_psychic and not has_psychic) or (needs_metal and not has_metal) or \
                   (needs_dark and not has_dark):
                    mismatched_pokemon += 1

        if mismatched_pokemon > 0:
            cs = max(0.0, cs - 0.4 * mismatched_pokemon)  # Heavy penalty for unplayable attackers

        # Check draw supporter deckout risk (excessive draw supporters without recovery)
        draw_supporters_count = sum(1 for c in deck if c.card_type == "Trainer" and any(k in c.card_name.lower() for k in {"research", "lillie", "carmine", "professor"}))
        has_recovery = any("pad" in c.card_name.lower() or "stretcher" in c.card_name.lower() or "rod" in c.card_name.lower() for c in deck)
        if draw_supporters_count >= 4 and not has_recovery:
            cs = max(0.0, cs - 0.2)  # Penalty for draw supporter spam risk

        return cs
    except Exception as e:
        return 0.0

def recovery_score(ct: dict) -> float:
    try:
        rs = min(1.0, ct.get("sup", 0) / 15.0)
        return min(1.0, rs + 0.1) if ct.get("rec", 0) >= 2 else (max(0.0, rs - 0.1) if ct.get("rec", 0) == 0 else rs)
    except Exception:
        return 0.0
