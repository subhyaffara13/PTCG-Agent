
def _get_oidc_http_handler(timeout: Optional[httpx.Timeout] = None) -> HTTPHandler:
    """
    Factory function to create HTTPHandler for OIDC requests.
    This function can be mocked in tests.

    Args:
        timeout: Optional timeout for HTTP requests. Defaults to 600.0 seconds with 5.0 connect timeout.

    Returns:
        HTTPHandler instance configured for OIDC requests.
    """
    if timeout is None:
        timeout = httpx.Timeout(timeout=600.0, connect=5.0)
    return HTTPHandler(timeout=timeout)

