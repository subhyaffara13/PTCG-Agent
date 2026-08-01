
def get_vertex_ai_allowed_incoming_headers(request: Request) -> dict:
    """
    Extract only the allowed headers from incoming request for Vertex AI pass-through.

    Uses an allowlist approach for security - only forwards headers we explicitly trust.
    This prevents accidentally forwarding sensitive headers like the LiteLLM auth token.

    Args:
        request: The FastAPI request object

    Returns:
        dict: Headers dictionary with only allowed headers
    """
    incoming_headers = _safe_get_request_headers(request)
    headers = {}
    for header_name in ALLOWED_VERTEX_AI_PASSTHROUGH_HEADERS:
        if header_name in incoming_headers:
            headers[header_name] = incoming_headers[header_name]
    return headers

