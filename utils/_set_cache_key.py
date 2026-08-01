
def _set_cache_key(
    cache: dict[_DispatchCacheKey, _DispatchCacheEntry],
    key: _DispatchCacheKey,
    entry: _DispatchCacheEntry,
) -> None:
    cache[key] = entry

