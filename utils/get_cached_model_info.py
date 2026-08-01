
def get_cached_model_info():
    """
    Lazy import and cache get_model_info to avoid circular imports.

    This function is used by bedrock transformation classes that need get_model_info
    but cannot import it at module level due to circular import issues.
    The function is cached after first use to avoid performance impact.
    """
    global _get_model_info
    if _get_model_info is None:
        from litellm import get_model_info

        _get_model_info = get_model_info
    return _get_model_info

