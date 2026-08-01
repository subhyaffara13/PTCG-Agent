
def validate_loopback_redirect_uri(redirect_uri: str) -> None:
    """Require a loopback ``redirect_uri`` (OAuth 2.1 §4.1.2.1 + RFC 8252
    §7.3 native-app pattern). MCP clients are native apps that listen on
    a localhost port; rejecting non-loopback URIs prevents a malicious
    client from pointing the callback at its own server to capture the
    authorization code — the credential-theft primitive behind VERIA-57
    and pNr1PHa9.

    Accepts the literal ``localhost`` plus any IP in the loopback ranges
    (IPv4 ``127.0.0.0/8`` and IPv6 ``::1``). A string match on
    ``"127.0.0.1"`` alone would miss ``127.0.0.2`` and the full-form
    IPv6 loopback ``0:0:0:0:0:0:0:1``.
    """
    parsed = _parse_redirect_uri_for_validation(redirect_uri)
    if parsed.scheme not in ("http", "https"):
        _oauth_invalid_request(
            f"redirect_uri scheme {parsed.scheme!r} is not allowed; use http or https.",
        )
    if parsed.fragment:
        _oauth_invalid_request(
            "redirect_uri must not contain a URL fragment (#...).",
        )
    host = (parsed.hostname or "").lower()
    if host == "localhost":
        return
    try:
        if ip_address(host).is_loopback:
            return
    except ValueError:
        # Unparseable host (malformed IPv6, etc.) — treat as invalid,
        # don't let it bubble up as a 500.
        pass
    _oauth_invalid_request(
        "redirect_uri must use a loopback host (localhost or 127.0.0.0/8).",
        hint="Native MCP clients should register a callback on http://127.0.0.1:<port>/...",
    )

