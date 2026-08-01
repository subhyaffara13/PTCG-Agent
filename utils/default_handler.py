
def default_handler(
        url: str,
        method: str,
        timeout: Optional[float],
        headers: List[Tuple[str, str]],
        data: bytes,
) -> Callable[[], None]:
    """Default handler that implements HTTP/HTTPS connections.

    Used by the push_to_gateway functions. Can be re-used by other handlers."""

    return _make_handler(url, method, timeout, headers, data, HTTPHandler)

