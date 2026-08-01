from typing import List
import logging

logger = logging.getLogger(__name__)

def sort_actions_heuristically(candidates: List[str], profile: str, game_state: dict) -> List[str]:
    try:
        from cb_agents.turn_planner_sort import sort_actions_heuristically as _impl
        return _impl(candidates, profile, game_state)
    except Exception:
        return candidates
