
def _get_cached_custom_logger():
    """
    Get cached CustomLogger class.
    Lazy imports on first call to avoid loading custom_logger at import time.
    Subsequent calls use cached class for better performance.
    """
    global _CustomLogger
    if _CustomLogger is None:
        from litellm.integrations.custom_logger import CustomLogger

        _CustomLogger = CustomLogger
    return _CustomLogger

