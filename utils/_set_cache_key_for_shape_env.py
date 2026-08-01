
def _set_cache_key_for_shape_env(
    cache: dict[_DispatchCacheKey, _DispatchCacheEntry],
    key: _DispatchCacheKey,
    entry: _DispatchCacheEntry,
) -> None:
    key.strip_shape_env()
    cache[key] = entry

