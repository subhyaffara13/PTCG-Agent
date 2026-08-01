
def clear_cached_imports() -> None:
    """Clear all cached imports. Useful for testing or memory management."""
    global _LiteLLMLogging, _coroutine_checker, _set_callbacks
    _LiteLLMLogging = None
    _coroutine_checker = None
    _set_callbacks = None

