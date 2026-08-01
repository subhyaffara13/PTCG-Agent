
def _parse_request_body(body: Optional[bytes], content_type: str = "") -> Any:
    """
    Parses a request body, handling bytes and string types, and different content types.

    Args:
        body (Optional[bytes]): The request body.
        content_type (str): The content type of the request body, e.g., "application/json",
            "application/x-www-form-urlencoded", or "text/plain". If empty, attempts
            to parse as JSON.

    Returns:
        Parsed body (dict, str, or None).
        - JSON: Decodes if content_type is "application/json" or None (fallback).
        - URL-encoded: Parses if content_type is "application/x-www-form-urlencoded".
        - Plain text: Returns string if content_type is "text/plain".
        - None: Returns if body is None, UTF-8 decode fails, or content_type is unknown.
    """
    if body is None:
        return None
    try:
        body_str = body.decode("utf-8")
    except (UnicodeDecodeError, AttributeError):
        return None
    content_type = content_type.lower()
    if not content_type or "application/json" in content_type:
        try:
            return json.loads(body_str)
        except (TypeError, ValueError):
            return body_str
    if "application/x-www-form-urlencoded" in content_type:
        parsed_query = urllib.parse.parse_qs(body_str)
        result = {k: v[0] for k, v in parsed_query.items()}
        return result
    if "text/plain" in content_type:
        return body_str
    return None

