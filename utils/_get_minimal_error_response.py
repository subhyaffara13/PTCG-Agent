
def _get_minimal_error_response() -> httpx.Response:
    """Get a cached minimal httpx.Response object for error cases."""
    global _MINIMAL_ERROR_RESPONSE
    if _MINIMAL_ERROR_RESPONSE is None:
        _MINIMAL_ERROR_RESPONSE = httpx.Response(
            status_code=400,
            request=httpx.Request(method="GET", url="https://litellm.ai"),
        )
    return _MINIMAL_ERROR_RESPONSE

