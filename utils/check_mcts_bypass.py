from typing import List

def check_mcts_bypass(candidates: List[str], game_state: dict, rules: dict | None = None):
    from cb_agents.heuristic_pipeline import check_mcts_bypass as _impl
    return _impl(candidates, game_state, rules or {})
