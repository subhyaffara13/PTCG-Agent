
def _resolve_timeout(
    optional_params: GenericLiteLLMParams,
    kwargs: Dict[str, Any],
    custom_llm_provider: str,
    default_timeout: float = 600.0,
) -> float:
    """
    Resolve timeout value from various sources and handle httpx.Timeout objects.

    Args:
        optional_params: GenericLiteLLMParams object containing timeout
        kwargs: Additional kwargs that may contain request_timeout
        custom_llm_provider: Provider name for httpx timeout support check
        default_timeout: Default timeout value to use

    Returns:
        Resolved timeout as float
    """
    timeout = (
        optional_params.timeout
        or kwargs.get("request_timeout", default_timeout)
        or default_timeout
    )

    # Handle httpx.Timeout objects
    if isinstance(timeout, httpx.Timeout):
        if supports_httpx_timeout(custom_llm_provider) is False:
            # Extract read timeout for providers that don't support httpx.Timeout
            read_timeout = timeout.read or default_timeout
            return float(read_timeout)
        else:
            # For providers that support httpx.Timeout, we still need to return a float
            # This case might need to be handled differently based on the actual use case
            return float(timeout.read or default_timeout)

    # Handle None case
    if timeout is None:
        return float(default_timeout)

    # Handle numeric values (int, float, string representations)
    return float(timeout)

