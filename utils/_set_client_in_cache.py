
def _set_client_in_cache(client_cache_key: str, vertex_llm_model: Any):
    litellm.in_memory_llm_clients_cache.set_cache(
        key=client_cache_key,
        value=vertex_llm_model,
        ttl=_DEFAULT_TTL_FOR_HTTPX_CLIENTS,
    )

