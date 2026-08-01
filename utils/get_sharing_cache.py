
def get_sharing_cache() -> CacheType:
    """Return the most recent sharing cache -- thread specific."""
    return _SHARING_STACK[threading.get_ident()][-1]

