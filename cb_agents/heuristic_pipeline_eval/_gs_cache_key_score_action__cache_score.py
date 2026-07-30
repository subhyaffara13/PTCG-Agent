from . import _HAS_CPP_SCORE, _SCORE_CACHE_MAX, _ptcg_core, _score_action_cache, _score_action_cache_keys, logger
from ._score_action_python import _score_action_python

def _gs_cache_key(gs: dict) -> tuple:
    return (
        gs.get("turn_number"), gs.get("my_prizes"), gs.get("opponent_prizes"),
        gs.get("my_active_hp"), gs.get("opponent_active_hp"),
        gs.get("my_deck_count"), gs.get("opponent_deck_count"),
        tuple(sorted(gs.get("my_hand", []))),
        tuple(str(x) for x in gs.get("my_bench", [])),
        gs.get("stadium_card"),
    )

def score_action(action: str, gs: dict, threat: float = 0.0) -> float:
    key = (action, _gs_cache_key(gs), threat)
    cached = _score_action_cache.get(key)
    if cached is not None:
        return cached
    if _HAS_CPP_SCORE and _ptcg_core is not None:
        try:
            val = _ptcg_core.score_action(gs, action)
            _cache_score(key, val)
            return val
        except Exception as e:
            logger.debug(f"C++ score_action failed: {e}. Falling back to Python.")
    val = _score_action_python(action, gs, threat)
    _cache_score(key, val)
    return val

def _cache_score(key: tuple, val: float):
    if len(_score_action_cache_keys) >= _SCORE_CACHE_MAX:
        old = _score_action_cache_keys.pop(0)
        _score_action_cache.pop(old, None)
    if key not in _score_action_cache:
        _score_action_cache[key] = val
        _score_action_cache_keys.append(key)

