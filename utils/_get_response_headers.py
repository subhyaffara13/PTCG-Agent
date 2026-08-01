
def _get_response_headers(original_exception: Exception) -> Optional[httpx.Headers]:
    """
    Extract and return the response headers from an exception, if present.

    Used for accurate retry logic.
    """
    _response_headers: Optional[httpx.Headers] = None
    try:
        _response_headers = getattr(original_exception, "headers", None)
        error_response = getattr(original_exception, "response", None)
        if not _response_headers and error_response:
            _response_headers = getattr(error_response, "headers", None)
        if not _response_headers:
            _response_headers = getattr(
                original_exception, "litellm_response_headers", None
            )
    except Exception:
        return None

    return _response_headers

