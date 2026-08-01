
def _get_client_from_cache(client_cache_key: str):
    return litellm.in_memory_llm_clients_cache.get_cache(client_cache_key)

