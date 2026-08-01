
def is_network_error(exc: Exception) -> bool:
    """True for transport-layer failures (connection refused, DNS, TLS, timeout)
    as opposed to HTTP protocol errors (4xx/5xx with a valid response)."""
    return isinstance(exc, httpx.TransportError)

