
def _get_embedding_config_cache() -> InMemoryCache:
    global _embedding_config_cache
    if _embedding_config_cache is None:
        _embedding_config_cache = InMemoryCache(
            max_size_in_memory=_EMBEDDING_CONFIG_CACHE_MAX_SIZE,
            default_ttl=_EMBEDDING_CONFIG_CACHE_TTL,
        )
    return _embedding_config_cache

