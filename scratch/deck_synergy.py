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
    t_map = {"{R}": "fire", "{W}": "water", "{G}": "grass", "{L}": "lightning", "{F}": "fighting", "{P}": "psychic", "{D}": "darkness", "{M}": "metal"}
    for pt in p_types:
        exp = t_map.get(pt, "none")
        if exp != "none" and not any(exp in en for en in e_names):
            penalty += SYNERGY_MISSING_ENERGY_PENALTY
    s2 = sum(1 for c in deck if details.get(str(c["card_id"]), {}).get("stage") == "Stage 2")
    rc = sum(1 for c in deck if c.get("card_name", "").lower() == "rare candy")
    if s2 > rc:
        penalty += SYNERGY_STAGE2_NO_CANDY_PENALTY * (s2 - rc)
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
