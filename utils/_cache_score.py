
def _cache_score(key: tuple, val: float):
    if len(_score_action_cache_keys) >= _SCORE_CACHE_MAX:
        old = _score_action_cache_keys.pop(0)
        _score_action_cache.pop(old, None)
    if key not in _score_action_cache:
        _score_action_cache[key] = val
        _score_action_cache_keys.append(key)


def _cache_score(key: tuple, val: float):
    if len(_score_action_cache_keys) >= _SCORE_CACHE_MAX:
        old = _score_action_cache_keys.pop(0)
        _score_action_cache.pop(old, None)
    if key not in _score_action_cache:
        _score_action_cache[key] = val
        _score_action_cache_keys.append(key)

