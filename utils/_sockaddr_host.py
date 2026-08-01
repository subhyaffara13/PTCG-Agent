
def _sockaddr_host(sockaddr: Any) -> str:
    """Return the host element of a ``getaddrinfo`` sockaddr as ``str``.

    ``getaddrinfo`` with ``IPPROTO_TCP`` returns AF_INET / AF_INET6 sockaddrs
    whose first element is always a host string. mypy types it as
    ``str | int`` (since sockaddrs for other families can hold ints), so we
    narrow at the boundary. Fail closed if the stdlib ever returns something
    unexpected — a non-string here would mean we have no IP to check against
    the SSRF blocklist.
    """
    host = sockaddr[0]
    if not isinstance(host, str):
        raise SSRFError(f"getaddrinfo returned non-string host: {host!r}")
    return host

