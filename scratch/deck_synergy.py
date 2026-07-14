from scratch.configs import (SYNERGY_MULTI_TYPE_PENALTY, SYNERGY_MULTI_BASIC_ENERGY_PENALTY,
    SYNERGY_MISSING_ENERGY_PENALTY, SYNERGY_STAGE2_NO_CANDY_PENALTY,
    SYNERGY_UNDER_COPIED_BASIC_PENALTY, SYNERGY_AREA_PENALTY_MULT,
    SYNERGY_AREA_PENALTY_PER, SYNERGY_RATIO_PENALTY_MULT, SYNERGY_RATIO_PENALTY_PER)

_AREA_LIMITS = {"pkmn_max": 20, "pkmn_min": 10, "trainer_min": 25, "energy_min": 8, "energy_max": 16}

def evaluate_deck_penalties(deck: list, details: dict) -> float:
    penalty = 0.0
    p_types = {details.get(str(c["card_id"]), {}).get("element_type", "") for c in deck if c.get("card_type") == "Pokemon"}
    p_types.discard("")
    e_names = {c.get("card_name", "").lower() for c in deck if c.get("card_type") == "Energy"}
    if len(p_types) > 2:
        penalty += SYNERGY_MULTI_TYPE_PENALTY * (len(p_types) - 2)
    basic_energy_names = {en for en in e_names if "basic" in en}
    if len(basic_energy_names) > 2:
        penalty += SYNERGY_MULTI_BASIC_ENERGY_PENALTY * (len(basic_energy_names) - 2)
    t_map = {
        "{R}": ["{r}", "fire"],
        "{W}": ["{w}", "water"],
        "{G}": ["{g}", "grass"],
        "{L}": ["{l}", "lightning"],
        "{F}": ["{f}", "fighting"],
        "{P}": ["{p}", "psychic"],
        "{D}": ["{d}", "darkness"],
        "{M}": ["{m}", "metal"]
    }
    for pt in p_types:
        keywords = t_map.get(pt, [])
        if keywords:
            # Proportional energy check: must have at least 6 matching energy cards for each active type
            matching_energy_count = sum(1 for c in deck if c.get("card_type") == "Energy" and any(kw in c.get("card_name", "").lower() for kw in keywords))
            if matching_energy_count < 6:
                penalty += 150.0 * (6 - matching_energy_count)
                
    # Useless basic energy check
    energy_types_in_deck = set()
    for c in deck:
        if c.get("card_type") == "Energy":
            name = c.get("card_name", "").lower()
            for k in t_map.keys():
                if k.lower() in name and "basic" in name:
                    energy_types_in_deck.add(k)
    for et in energy_types_in_deck:
        if et not in p_types:
            useless_count = sum(1 for c in deck if c.get("card_type") == "Energy" and et.lower() in c.get("card_name", "").lower() and "basic" in c.get("card_name", "").lower())
            penalty += 150.0 * useless_count
            
    s2 = sum(1 for c in deck if details.get(str(c["card_id"]), {}).get("stage") == "Stage 2")
    rc = sum(1 for c in deck if c.get("card_name", "").lower() == "rare candy")
    if s2 > rc:
        penalty += SYNERGY_STAGE2_NO_CANDY_PENALTY * (s2 - rc)
        
    # Evolutionary line checks
    pokemon_names_in_deck = {c.get("card_name", "") for c in deck if c.get("card_type") == "Pokemon"}
    basic_names = {c.get("card_name", "") for c in deck if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"}
    
    # 1. Basic evolution check: penalize basic cards that can evolve but have no evolution in the deck
    for name in basic_names:
        has_evo_in_pool = any(val.get("previous_stage") == name for val in details.values())
        if has_evo_in_pool:
            has_evo_in_deck = any(details.get(str(x["card_id"]), {}).get("previous_stage") == name for x in deck)
            if not has_evo_in_deck:
                penalty += 300.0
                
    # 2. Pre-evolution check: penalize evolved stage cards that have no corresponding pre-evolution (taking rare candy into account)
    for c in deck:
        if c.get("card_type") == "Pokemon":
            cid = str(c["card_id"])
            prev = details.get(cid, {}).get("previous_stage", "")
            if prev and prev not in pokemon_names_in_deck:
                stage = details.get(cid, {}).get("stage", "")
                if stage == "Stage 2":
                    stage1_val = next((val for val in details.values() if val.get("card_name") == prev), None)
                    basic_name = stage1_val.get("previous_stage", "") if stage1_val else ""
                    has_rare_candy = any(x.get("card_name", "").lower() == "rare candy" for x in deck)
                    has_basic = basic_name in pokemon_names_in_deck if basic_name else False
                    has_stage1 = prev in pokemon_names_in_deck
                    if not (has_stage1 or (has_basic and has_rare_candy)):
                        penalty += 300.0
                else:
                    # Stage 1 requires its basic
                    if prev not in pokemon_names_in_deck:
                        penalty += 300.0

    copies = {}
    for c in deck:
        if c.get("card_type") == "Pokemon":
            cid = str(c["card_id"])
            copies[cid] = copies.get(cid, 0) + 1
    for cid, qty in copies.items():
        stage = details.get(cid, {}).get("stage", "Basic")
        if qty < 3 and stage == "Basic":
            penalty += SYNERGY_UNDER_COPIED_BASIC_PENALTY * (3 - qty)
    n_pkmn = sum(1 for c in deck if c.get("card_type") == "Pokemon")
    n_trainers = sum(1 for c in deck if c.get("card_type") == "Trainer")
    n_energy = sum(1 for c in deck if c.get("card_type") == "Energy")
    if n_pkmn > _AREA_LIMITS["pkmn_max"]:
        penalty += SYNERGY_AREA_PENALTY_MULT + SYNERGY_AREA_PENALTY_PER * (n_pkmn - _AREA_LIMITS["pkmn_max"])
    elif n_pkmn < _AREA_LIMITS["pkmn_min"]:
        penalty += SYNERGY_AREA_PENALTY_MULT + SYNERGY_AREA_PENALTY_PER * (_AREA_LIMITS["pkmn_min"] - n_pkmn)
    if n_trainers < _AREA_LIMITS["trainer_min"]:
        penalty += SYNERGY_RATIO_PENALTY_MULT + SYNERGY_RATIO_PENALTY_PER * (_AREA_LIMITS["trainer_min"] - n_trainers)
    if n_energy < _AREA_LIMITS["energy_min"]:
        penalty += SYNERGY_RATIO_PENALTY_MULT + SYNERGY_RATIO_PENALTY_PER * (_AREA_LIMITS["energy_min"] - n_energy)
    elif n_energy > _AREA_LIMITS["energy_max"]:
        penalty += SYNERGY_RATIO_PENALTY_MULT + SYNERGY_RATIO_PENALTY_PER * (n_energy - _AREA_LIMITS["energy_max"])
    return penalty

from scratch.deck_synergy_graph import get_global_synergy_graph, score_deck_synergy
from scratch.configs import SYNERGY_PMI_WEIGHT, SYNERGY_PENALTY_WEIGHT

def evaluate_deck_synergy(deck: list, details: dict) -> float:
    penalty = evaluate_deck_penalties(deck, details)
    graph = get_global_synergy_graph()
    pmi_score = score_deck_synergy(deck, graph)
    return (SYNERGY_PMI_WEIGHT * pmi_score) - (SYNERGY_PENALTY_WEIGHT * penalty)
