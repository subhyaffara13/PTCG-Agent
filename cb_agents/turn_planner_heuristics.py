import logging
from typing import List
from cb_agents.card_registry import CardRegistry
logger = logging.getLogger(__name__)
_registry = CardRegistry()

from cb_agents.constants import ABILITY_DRAW as _ABILITY_DRAW_KEYWORDS, SCALING_ATTACKERS

def has_type_advantage(my_active_id, opp_active_id) -> bool:
    """Check if our active Pokémon has type advantage (2x weakness) over opponent's active."""
    try:
        if my_active_id is None or opp_active_id is None:
            return False
        my_type = _registry.card_poke_type.get(int(my_active_id), "")
        opp_weakness = _registry.card_weakness.get(int(opp_active_id), "")
        if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
            return True
    except Exception:
        pass
    return False

def _hand_strength(game_state: dict) -> str:
    hand = game_state.get("my_hand", [])
    hand_size = len(hand) if isinstance(hand, list) else 0
    if hand_size <= 2:
        return "weak"
    elif hand_size <= 4:
        return "medium"
    return "strong"

def has_draw_remaining(candidates: List[str]) -> bool:
    for cand in candidates:
        try:
            if cand.startswith("play_trainer:"):
                name = cand.split(":", 1)[1].lower()
                if any(dk in name for dk in {"research", "iono", "judge", "concealed cards",
                                              "flower selecting", "shining arcana", "colress"}):
                    return True
            if cand.startswith("ability:"):
                target = cand.split(":", 1)[1].lower()
                if any(dk in target for dk in _ABILITY_DRAW_KEYWORDS):
                    return True
        except IndexError:
            continue
    return False

def check_mcts_bypass(candidates: List[str], game_state: dict, rules: dict | None = None):
    from cb_agents.heuristic_pipeline import check_mcts_bypass as _impl
    return _impl(candidates, game_state, rules or {})

def sort_actions_heuristically(candidates: List[str], profile: str, game_state: dict) -> List[str]:
    from cb_agents.turn_planner_sort import sort_actions_heuristically as _impl
    return _impl(candidates, profile, game_state)
