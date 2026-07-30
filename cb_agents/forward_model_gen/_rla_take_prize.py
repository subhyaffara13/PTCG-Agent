from cb_agents.forward_model_gen._cache_legal_helpers import _legal_actions_cache
from ._cache_legal_helpers import _cache_legal

def _rla_handle_take_prize(gs, ck):
    my_prizes = gs.get("my_prizes", [])
    if isinstance(my_prizes, list) and my_prizes:
        n = min(gs.get("prize_count", 1), len(my_prizes))
        actions = [f"take_prize:{i}" for i in range(n)]
    else:
        actions = [f"take_prize:{i}" for i in range(gs.get("prize_count", 1))]
    gs["legal_actions"] = actions
    _cache_legal(ck, actions)
