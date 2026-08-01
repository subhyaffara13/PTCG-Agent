
def _proxy_base_url(http_request: Request) -> str:
    """Return the proxy's base URL as seen by the caller, without trailing slash."""
    return str(http_request.base_url).rstrip("/")

