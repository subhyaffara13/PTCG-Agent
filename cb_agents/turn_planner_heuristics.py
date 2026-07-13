import logging
from typing import List
from cb_agents.card_registry import CardRegistry
logger = logging.getLogger(__name__)
_registry = CardRegistry()

from cb_agents.constants import ABILITY_DRAW as _ABILITY_DRAW_KEYWORDS, SCALING_ATTACKERS

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

from cb_agents.heuristic_pipeline import _thinning_value, _pick_best_search, _dead_weight_heuristic, check_mcts_bypass
from cb_agents.turn_planner_sort import _has_evolution_target, sort_actions_heuristically, _EARLY_BENCH_ORDER
