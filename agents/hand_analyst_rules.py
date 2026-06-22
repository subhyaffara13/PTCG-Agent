"""
agents/hand_analyst_rules.py
Rules and sorting logic for HandAnalyst.
"""
from typing import List
from agents.hand_analyst_config import unpack_ha_config  # noqa: F401

def resolve_priority_profile(metrics: dict, config: dict, phase: str) -> str:
    opp_prizes = metrics["opponent_prizes"]
    hand_score = metrics["hand_score"]
    
    if opp_prizes <= config["closing_opp_prizes"] and metrics["has_attacker"]:
        return "closing"
    elif metrics["has_attacker"] and metrics["has_energy"] and hand_score > config["aggro_push_hand_score"]:
        return "aggro_push"
    elif (metrics["has_basic"] and not metrics["has_energy"]) or (metrics["has_evolution"] and not metrics["has_basic"]) or hand_score < config["setup_hand_score"]:
        return "setup"
    elif metrics["control_count"] >= config["disruption_control_count"] and opp_prizes <= config["disruption_opp_prizes"]:
        return "disruption"
    elif metrics["deck_remaining"] < config["stall_deck_remaining"] and not metrics["has_attacker"]:
        return "stall"
    return "setup" if phase == 'early' else "aggro_push"

def get_sorted_top_play(hand_cards_data: List[tuple]) -> str:
    def sort_key(item):
        card, ev = item
        ctype = getattr(card, "card_type", "Trainer")
        if ctype == "Pokemon" or (hasattr(ctype, "name") and ctype.name == "POKEMON"):
            type_priority = 3
        elif ctype == "Trainer" or (hasattr(ctype, "name") and ctype.name == "TRAINER"):
            type_priority = 2
        else:
            type_priority = 1
        return (ev, type_priority)

    hand_cards_data.sort(key=sort_key, reverse=True)
    top_play_card = hand_cards_data[0][0]
    return getattr(top_play_card, "card_name", getattr(top_play_card, "card_id", "none"))
