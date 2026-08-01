
def add_fallback_headers_to_response(
    response: Any,
    attempted_fallbacks: int,
) -> Any:
    """
    Add fallback headers to the response

    Args:
        response: The response to add the headers to
        attempted_fallbacks: The number of fallbacks attempted

    Returns:
        The response with the headers added

    Note: It's intentional that we don't add max_fallbacks in response headers
    Want to avoid bloat in the response headers for performance.
    """
    fallback_headers = {
        "x-litellm-attempted-fallbacks": attempted_fallbacks,
    }
    return _add_headers_to_response(response, fallback_headers)

