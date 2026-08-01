
def _cache_legal(key: tuple, actions: list):
    if len(_legal_actions_cache_order) >= _LEGAL_CACHE_MAX:
        old = _legal_actions_cache_order.pop(0)
        _legal_actions_cache.pop(old, None)
    if key not in _legal_actions_cache:
        _legal_actions_cache[key] = actions
        _legal_actions_cache_order.append(key)


def _cache_legal(key: tuple, actions: list):
    if len(_legal_actions_cache_order) >= _LEGAL_CACHE_MAX:
        old = _legal_actions_cache_order.pop(0)
        _legal_actions_cache.pop(old, None)
    if key not in _legal_actions_cache:
        _legal_actions_cache[key] = actions
        _legal_actions_cache_order.append(key)

