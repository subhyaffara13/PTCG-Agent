
def _get_cached_llm_caching_handler():
    """
    Get cached LLMCachingHandler class.
    Lazy imports on first call to avoid loading caching_handler at import time.
    Subsequent calls use cached class for better performance.
    """
    global _LLMCachingHandler
    if _LLMCachingHandler is None:
        from litellm.caching.caching_handler import LLMCachingHandler

        _LLMCachingHandler = LLMCachingHandler
    return _LLMCachingHandler

