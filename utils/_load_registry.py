
def _load_registry() -> Registry:
    """Resolve the registry from the local cache or the Hub.

    No hardcoded list: if the Hub is unreachable and no cached copy exists, an
    empty registry is returned (i.e. no agent is detected).
    """
    path = constants.AGENT_HARNESSES_PATH

    # 1. Use the cached file if it was refreshed within the last 24 hours.
    if cached := _read_cached_registry(path, max_age=_REGISTRY_TTL_SECONDS):
        return cached

    # 2. Otherwise refresh it from the Hub and persist it for next time.
    if (fetched := _fetch_registry()) is not None:
        _write_cached_registry(path, fetched)
        return fetched

    # 3. Fetch failed: reuse a stale cache if available, else give up (no detection).
    if stale := _read_cached_registry(path, max_age=None):
        return stale
    return _EMPTY_REGISTRY

