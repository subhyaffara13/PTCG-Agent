
def _extract_redirect_url(response: Any, request_url: str) -> str:
    """Extract and resolve the redirect target from a response's Location header."""
    location = response.headers.get("location")
    if not isinstance(location, str) or not location:
        raise SSRFError("Redirect response has no Location header")
    # Resolve relative URLs against the request URL
    return str(httpx.URL(request_url).join(location))

