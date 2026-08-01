
def assert_same_origin(candidate_url: str, expected_url: str) -> None:
    """Verify ``candidate_url`` shares scheme, host, and port with ``expected_url``.

    Use when an upstream API returns a URL meant for follow-up requests
    (e.g. an async-job polling URL that will be hit with the operator's
    API key in the headers). The upstream is trusted because the operator
    configured ``api_base``, but the URL it hands back must actually point
    back at the same origin or we'd be blindly forwarding credentials
    wherever the upstream told us to.

    Hostnames are compared case-insensitively. Default ports are made
    explicit (HTTP→80, HTTPS→443) so ``https://api.example.com:443/...``
    and ``https://api.example.com/...`` are treated as the same origin.

    Error messages identify *which* component mismatched but never echo
    the operator's ``expected`` host or the candidate's hostname back to
    the caller — in the SSRF threat model the caller is the attacker,
    and reflecting host info would be a secondary leak of operator
    infrastructure details.
    """
    candidate = urlparse(candidate_url)
    expected = urlparse(expected_url)

    if candidate.scheme not in _ALLOWED_SCHEMES:
        raise SSRFError("URL scheme is not allowed")

    if candidate.scheme != expected.scheme:
        raise SSRFError("Origin mismatch on scheme")

    candidate_host = _normalize_host(candidate.hostname or "")
    expected_host = _normalize_host(expected.hostname or "")
    if not candidate_host or candidate_host != expected_host:
        raise SSRFError("Origin mismatch on host")

    default_port = 443 if candidate.scheme == "https" else 80
    candidate_port = candidate.port if candidate.port is not None else default_port
    expected_port = expected.port if expected.port is not None else default_port
    if candidate_port != expected_port:
        raise SSRFError("Origin mismatch on port")

