
def _validate_trusted_http_redirect_shape(parsed: ParseResult) -> bool:
    """Return True when ``parsed`` is an allowlisted native callback (caller may return)."""
    if parsed.scheme not in ("http", "https"):
        if _matches_trusted_native_redirect_uri(parsed):
            return True
        _oauth_invalid_request(
            f"redirect_uri scheme {parsed.scheme!r} is not allowed; use http/https "
            "or a registered native callback (e.g. cursor://).",
            hint="Add the full URI to MCP_TRUSTED_NATIVE_REDIRECT_URIS for custom native clients.",
        )
    if parsed.fragment:
        _oauth_invalid_request(
            "redirect_uri must not contain a URL fragment (#...).",
        )
    if not parsed.netloc:
        _oauth_invalid_request(
            "redirect_uri must include a host (e.g. https://your-host/path).",
        )
    if parsed.username is not None or parsed.password is not None:
        _oauth_invalid_request(
            "redirect_uri must not contain userinfo (user:pass@host).",
        )
    if "\\" in parsed.netloc:
        _oauth_invalid_request(
            "redirect_uri host must not contain backslashes.",
        )
    return False

