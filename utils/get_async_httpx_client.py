
def get_async_httpx_client(
    llm_provider: Union[LlmProviders, httpxSpecialProvider],
    params: Optional[dict] = None,
    shared_session: Optional["ClientSession"] = None,
) -> AsyncHTTPHandler:
    """
    Retrieves the async HTTP client from the cache
    If not present, creates a new client

    Caches the new client and returns it.
    """
    _params_key_name = ""
    if params is not None:
        for key, value in params.items():
            try:
                _params_key_name += f"{key}_{value}"
            except Exception:
                pass

    _cache_key_name = "async_httpx_client" + _params_key_name + llm_provider

    # Lazily initialize the global in-memory client cache to avoid relying on
    # litellm globals being fully populated during import time.
    cache = getattr(litellm, "in_memory_llm_clients_cache", None)
    if cache is None:
        from litellm.caching.llm_caching_handler import LLMClientCache

        cache = LLMClientCache()
        setattr(litellm, "in_memory_llm_clients_cache", cache)

    _cached_client = cache.get_cache(_cache_key_name)
    if _cached_client:
        return _cached_client

    if params is not None:
        # Filter out params that are only used for cache key, not for AsyncHTTPHandler.__init__
        handler_params = {
            k: v for k, v in params.items() if k != "disable_aiohttp_transport"
        }
        handler_params["shared_session"] = shared_session
        _new_client = AsyncHTTPHandler(**handler_params)
    else:
        _new_client = AsyncHTTPHandler(
            timeout=_DEFAULT_TIMEOUT,
            shared_session=shared_session,
        )

    cache.set_cache(
        key=_cache_key_name,
        value=_new_client,
        ttl=_DEFAULT_TTL_FOR_HTTPX_CLIENTS,
    )
    return _new_client

