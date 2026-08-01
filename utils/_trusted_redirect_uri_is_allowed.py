
def _trusted_redirect_uri_is_allowed(
    parsed: ParseResult,
    redirect_netloc: str,
    proxy_base: Optional[str],
) -> bool:
    if proxy_base:
        proxy_parsed = urlparse(proxy_base)
        if (
            parsed.scheme == proxy_parsed.scheme
            and redirect_netloc
            == _strip_default_port(proxy_parsed.scheme, proxy_parsed.netloc)
        ):
            return True

    host = (parsed.hostname or "").lower()
    if host == "localhost":
        return True
    try:
        if ip_address(host).is_loopback:
            return True
    except ValueError:
        pass

    if parsed.scheme == "https":
        for entry in _parse_trusted_redirect_origins():
            if _matches_trusted_origin_entry(redirect_netloc, entry):
                return True
    return False

