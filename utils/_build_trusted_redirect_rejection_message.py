
def _build_trusted_redirect_rejection_message(
    redirect_uri: str,
    parsed: ParseResult,
    redirect_netloc: str,
    proxy_base: Optional[str],
) -> str:
    """Build a client-facing rejection message.

    Intentionally omits the proxy's resolved scheme / host / port to avoid
    leaking internal network topology (e.g. ``http://litellm-internal:4000``)
    through an unauthenticated endpoint. Full diagnostic detail — including
    the computed proxy base — is logged server-side by the caller.
    """
    redirect_origin = _origin_label(parsed.scheme, redirect_netloc)
    proxy_parsed = urlparse(proxy_base) if proxy_base else None
    proxy_netloc_norm = (
        _strip_default_port(proxy_parsed.scheme, proxy_parsed.netloc)
        if proxy_parsed and proxy_parsed.netloc
        else ""
    )

    mismatch_parts: List[str] = []
    if proxy_parsed and proxy_parsed.netloc:
        if parsed.scheme != proxy_parsed.scheme:
            mismatch_parts.append(
                f"scheme: redirect_uri uses {parsed.scheme!r}, but the proxy "
                "resolved a different scheme "
                "(TLS often terminates at ingress — set PROXY_BASE_URL to https://… "
                "or trust X-Forwarded-Proto from your ingress)"
            )
        if redirect_netloc != proxy_netloc_norm:
            mismatch_parts.append(
                f"host/port: redirect_uri {redirect_netloc!r} does not match "
                "the proxy origin"
            )

    if mismatch_parts:
        return (
            f"redirect_uri origin ({redirect_origin}) does not match the proxy "
            "origin. " + "; ".join(mismatch_parts)
        )
    return (
        f"redirect_uri ({redirect_uri!r}) is not allowed: not same-origin with "
        f"the proxy origin, not loopback, and not listed in "
        f"{_TRUSTED_REDIRECT_ORIGINS_ENV}."
    )

