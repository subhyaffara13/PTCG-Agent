
def _write_byok_cred_cache(
    user_id: str, server_id: str, credential: Optional[str]
) -> None:
    """Write a credential value to the cache, evicting all entries if at capacity."""
    if len(_byok_cred_cache) >= _BYOK_CRED_CACHE_MAX_SIZE:
        _byok_cred_cache.clear()
    _byok_cred_cache[(user_id, server_id)] = (credential, time.monotonic())

