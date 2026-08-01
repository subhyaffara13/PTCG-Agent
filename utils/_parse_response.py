
def _parse_response(response: Any) -> Any:
    """
    Parses a response, attempting to decode JSON.

    Args:
        response: The response object to parse. This can be any type, but
            it is expected to have a `json()` method if it contains JSON.

    Returns:
        The parsed response. If the response contains valid JSON, the
        decoded JSON object (e.g., a dictionary or list) is returned.
        If the response does not have a `json()` method or if the JSON
        decoding fails, None is returned.
    """
    try:
        json_response = response.json()
        return json_response
    except Exception:
        # TODO(https://github.com/googleapis/google-auth-library-python/issues/1744):
        # Parse and return response payload as json based on different content types.
        return None

