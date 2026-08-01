
def _lazy_import_llm_client_cache(name: str) -> Any:
    """
    Handler for LLM client cache - has special logic for singleton instance.

    This one is different because:
    - "LLMClientCache" is the class itself
    - "in_memory_llm_clients_cache" is a singleton instance of that class
    So we need custom logic to handle both cases.
    """
    _globals = _get_litellm_globals()

    # If already cached, return it
    if name in _globals:
        return _globals[name]

    # Import the class
    module = importlib.import_module("litellm.caching.llm_caching_handler")
    LLMClientCache = getattr(module, "LLMClientCache")

    # If they want the class itself, return it
    if name == "LLMClientCache":
        _globals["LLMClientCache"] = LLMClientCache
        return LLMClientCache

    # If they want the singleton instance, create it (only once)
    if name == "in_memory_llm_clients_cache":
        instance = LLMClientCache()
        _globals["in_memory_llm_clients_cache"] = instance
        return instance

    raise AttributeError(f"LLM client cache lazy import: unknown attribute {name!r}")

