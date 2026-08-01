
def passthrough_redirect_handler(
        url: str,
        method: str,
        timeout: Optional[float],
        headers: List[Tuple[str, str]],
        data: bytes,
) -> Callable[[], None]:
    """
    Handler that automatically trusts redirect responses for all HTTP methods.

    Augments standard HTTPRedirectHandler capability by permitting PUT requests,
    preserving the method upon redirect, and passing through all headers and
    data from the original request. Only use this handler if you control or
    trust the source of redirect responses you encounter when making requests
    via the Prometheus client. This handler will simply repeat the identical
    request, including same method and data, to the new redirect URL."""

    return _make_handler(url, method, timeout, headers, data, _PrometheusRedirectHandler)

