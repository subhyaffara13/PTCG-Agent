
def _get_cached_caching_handler_response():
    """
    Get cached CachingHandlerResponse class.
    Lazy imports on first call to avoid loading caching_handler at import time.
    Subsequent calls use cached class for better performance.
    """
    global _CachingHandlerResponse
    if _CachingHandlerResponse is None:
        from litellm.caching.caching_handler import CachingHandlerResponse

        _CachingHandlerResponse = CachingHandlerResponse
    return _CachingHandlerResponse

