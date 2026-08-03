import time
from typing import Optional

def _prune_oauth_metadata_cache(now: Optional[float] = None) -> None:
    now = now if now is not None else time.time()
    expired_cache_keys = [
        cache_key
        for cache_key, (expires_at, _payload) in _OAUTH_METADATA_CACHE.items()
        if expires_at <= now
    ]
    for cache_key in expired_cache_keys:
        _OAUTH_METADATA_CACHE.pop(cache_key, None)

    if len(_OAUTH_METADATA_CACHE) > _OAUTH_METADATA_CACHE_MAX_SIZE:
        overflow = len(_OAUTH_METADATA_CACHE) - _OAUTH_METADATA_CACHE_MAX_SIZE
        cache_keys_by_expiry = sorted(
            _OAUTH_METADATA_CACHE,
            key=lambda cache_key: _OAUTH_METADATA_CACHE[cache_key][0],
        )
        for cache_key in cache_keys_by_expiry[:overflow]:
            _OAUTH_METADATA_CACHE.pop(cache_key, None)

    # Drop locks whose cache entry has been evicted and that aren't currently
    # held; held locks stay so in-flight callers continue to coalesce.
    for cache_key in list(_OAUTH_METADATA_FETCH_LOCKS):
        if cache_key in _OAUTH_METADATA_CACHE:
            continue
        lock = _OAUTH_METADATA_FETCH_LOCKS.get(cache_key)
        if lock is None or lock.locked():
            continue
        _OAUTH_METADATA_FETCH_LOCKS.pop(cache_key, None)

