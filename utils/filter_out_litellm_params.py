
def filter_out_litellm_params(kwargs: dict) -> dict:
    """
    Filter out LiteLLM internal parameters from kwargs dict.

    Returns a new dict containing only non-LiteLLM parameters that should be
    passed to external provider APIs.

    Args:
        kwargs: Dictionary that may contain LiteLLM internal parameters

    Returns:
        Dictionary with LiteLLM internal parameters filtered out

    Example:
        >>> kwargs = {"query": "test", "shared_session": session_obj, "metadata": {}}
        >>> filtered = filter_out_litellm_params(kwargs)
        >>> # filtered = {"query": "test"}
    """

    return {
        key: value for key, value in kwargs.items() if key not in all_litellm_params
    }

