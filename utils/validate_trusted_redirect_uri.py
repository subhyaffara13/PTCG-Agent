
def validate_trusted_redirect_uri(request: Request, redirect_uri: str) -> None:
    """Accept ``redirect_uri`` when it is (a) same-origin with the
    proxy's own request origin, (b) loopback, (c) listed in the
    ``MCP_TRUSTED_REDIRECT_ORIGINS`` ops allowlist, or (d) a built-in /
    env-configured native MCP client callback (e.g. ``cursor://``).

    Same-origin is VERIA-57's threat-model-safe equivalent of loopback:
    an attacker who can host content on the proxy's own HTTPS origin
    has already compromised the proxy, so the open-redirect + code-
    theft primitive that motivated the loopback-only rule does not
    apply. The same reasoning extends to ops-trusted first-party
    hosts (e.g. an internal web app registering as an OAuth client of
    the proxy on a sister domain).

    Allowlisted non-loopback hosts are accepted only when the
    redirect_uri scheme is ``https`` — an attacker on the network
    cannot elevate to https without controlling the host's TLS key.

    Use this in the discoverable OAuth proxy endpoints that serve both
    native clients and the proxy's UI / cross-origin web clients. The
    BYOK endpoints, which only serve native MCP clients, retain
    :func:`validate_loopback_redirect_uri`.
    """
    parsed = _parse_redirect_uri_for_validation(redirect_uri)
    if _validate_trusted_http_redirect_shape(parsed):
        return
    redirect_netloc = _strip_default_port(parsed.scheme, parsed.netloc)
    proxy_base = _resolve_proxy_base_for_redirect(request)
    if _trusted_redirect_uri_is_allowed(parsed, redirect_netloc, proxy_base):
        return
    _raise_trusted_redirect_uri_rejected(
        request, redirect_uri, parsed, redirect_netloc, proxy_base
    )

