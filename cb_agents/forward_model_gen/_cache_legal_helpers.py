from . import _LEGAL_CACHE_MAX, _get_prize_yield, _legal_actions_cache, _legal_actions_cache_order

def _count_high_prize_on_board(gs: dict) -> int:
    """Count how many high-prize (prize_yield>=2) Pokemon are on our board."""
    count = 0
    active = gs.get("my_active_pokemon", {})
    if isinstance(active, dict):
        if _get_prize_yield(str(active.get("card_name", ""))) >= 2:
            count += 1
    for bp in gs.get("my_bench", []):
        if isinstance(bp, dict):
            if _get_prize_yield(str(bp.get("card_name", ""))) >= 2:
                count += 1
    return count

def _cache_legal(key: tuple, actions: list):
    if len(_legal_actions_cache_order) >= _LEGAL_CACHE_MAX:
        old = _legal_actions_cache_order.pop(0)
        _legal_actions_cache.pop(old, None)
    if key not in _legal_actions_cache:
        _legal_actions_cache[key] = actions
        _legal_actions_cache_order.append(key)

def _legal_cache_key(gs: dict) -> tuple:
    return (
        gs.get("turn_number"), gs.get("select_prize"),
        gs.get("supporter_played_this_turn"),
        gs.get("boss_prob", 0.0),
        gs.get("prize_certainty", 0.0),
        frozenset(gs.get("prized_card_ids", {}).items()),
        tuple(sorted(gs.get("my_hand", []))),
        tuple(sorted(
            str(p.get("id")) for p in gs.get("my_bench", []) if isinstance(p, dict)
        )),
    )

