from typing import Any, Callable

def _get_lazy_import_registry() -> dict[str, Callable[[str], Any]]:
    """
    Build the registry that maps attribute names to their handler functions.

    This is called once, the first time someone accesses a lazy-loaded attribute.
    After that, we just look up the handler function in this dictionary.

    Returns:
        Dictionary like {"ModelResponse": _lazy_import_utils, ...}
    """
    global _LAZY_IMPORT_REGISTRY
    if _LAZY_IMPORT_REGISTRY is None:
        # Build the registry by going through each category and mapping
        # all the names in that category to their handler function
        _LAZY_IMPORT_REGISTRY = {}
        # For each category, map all its names to the handler function
        # Example: All names in UTILS_NAMES get mapped to _lazy_import_utils
        for name in COST_CALCULATOR_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_cost_calculator
        for name in LITELLM_LOGGING_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_litellm_logging
        for name in UTILS_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_utils
        for name in TOKEN_COUNTER_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_token_counter
        for name in LLM_CLIENT_CACHE_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_llm_client_cache
        for name in BEDROCK_TYPES_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_bedrock_types
        for name in TYPES_UTILS_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_types_utils
        for name in CACHING_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_caching
        for name in HTTP_HANDLER_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_http_handlers
        for name in DOTPROMPT_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_dotprompt
        for name in LLM_CONFIG_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_llm_configs
        for name in TYPES_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_types
        for name in LLM_PROVIDER_LOGIC_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_llm_provider_logic
        for name in UTILS_MODULE_NAMES:
            _LAZY_IMPORT_REGISTRY[name] = _lazy_import_utils_module

    return _LAZY_IMPORT_REGISTRY

