
def _get_http_client() -> HTTPHandler:
    """Get cached httpx client with SSL verification disabled."""
    return _get_httpx_client(params={"ssl_verify": False})

