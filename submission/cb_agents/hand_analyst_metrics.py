"""
agents/hand_analyst_metrics.py
Calculates hand score, priority profile, and top play action.
"""
from typing import List, Dict, Any
from cb_agents.hand_analyst_rules import unpack_ha_config, resolve_priority_profile, get_sorted_top_play
from cb_agents.hand_analyst_helpers import eval_hand_cards, get_multipliers_and_bonuses, eval_bricks_evo, apply_phase_bonuses

def calculate_hand_score_and_profile(
    hand: List[str], board: List[str], turn: int, opponent_prizes: int, deck_remaining: int,
    registry: Any, strategy_thresholds: Dict[str, Any], strategy_tips: Dict[str, Any]
) -> dict:
    ev_scores, hand_cards_data, flags = eval_hand_cards(hand, registry)
    if not ev_scores:
        return {"hand_score": 0.0, "priority_profile": "setup", "top_play": "none", "reasoning_chain": "Empty evaluations."}

    cfg = unpack_ha_config(strategy_thresholds)
    phase = 'early' if turn <= 3 else ('mid' if turn <= 8 else 'late')
    avg_ev = sum(ev_scores) / len(ev_scores)

    multiplier, bonus = get_multipliers_and_bonuses(flags, strategy_tips, cfg, flags["supporter_count"])
    brick_penalty, evo_bonus = eval_bricks_evo(hand, board, registry, cfg)
    bonus += brick_penalty
    multiplier += evo_bonus
    bonus += apply_phase_bonuses(phase, flags, hand_cards_data, cfg)

    hand_score = min(1.0, max(0.0, (avg_ev + bonus) * multiplier))
    has_attacker = any(getattr(c[0], "damage_output", 0) > 0 for c in hand_cards_data if getattr(c[0], "card_type", "") == "Pokemon" or getattr(getattr(c[0], "card_type", None), "name", "") == "POKEMON")
    has_evolution = any(getattr(c[0], "card_type", "") == "Pokemon" and "Stage" in getattr(c[0], "card_name", "") for c in hand_cards_data)
    control_count = sum(1 for c in hand_cards_data if getattr(c[0], "archetype", "") == "control")

    metrics = {
        "opponent_prizes": opponent_prizes, "hand_score": hand_score, "has_attacker": has_attacker,
        "has_energy": flags["has_energy"], "has_basic": flags["has_basic"], "has_evolution": has_evolution,
        "control_count": control_count, "deck_remaining": deck_remaining
    }
    priority_profile = resolve_priority_profile(metrics, cfg, phase)
    top_play = get_sorted_top_play(hand_cards_data)

    return {
        "hand_score": round(hand_score, 4),
        "priority_profile": priority_profile,
        "top_play": top_play,
        "reasoning_chain": f"Hand score {round(hand_score, 4)}, profile {priority_profile} resolved."
    }
