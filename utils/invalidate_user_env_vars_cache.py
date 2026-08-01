
def invalidate_user_env_vars_cache(user_id: str, server_id: str) -> None:
    """Drop a cached entry after the user stores or clears their env var values
    so the next request reads the fresh value instead of a stale one."""
    _user_env_vars_cache.pop((user_id, server_id), None)

