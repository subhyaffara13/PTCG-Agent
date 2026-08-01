
def _matches_trusted_native_redirect_uri(parsed) -> bool:
    """Allowlisted private-use / custom-scheme OAuth callbacks for native MCP clients."""
    if parsed.fragment:
        return False
    # Query strings are not part of registered redirect_uris (RFC 6749 §3.1.2).
    # Rejecting them prevents allowlist bypass via ``.../callback?injected=...``.
    if parsed.query:
        return False
    if not parsed.netloc:
        return False
    if parsed.username is not None or parsed.password is not None:
        return False
    if "\\" in parsed.netloc:
        return False

    normalized = _normalize_native_redirect_uri(parsed)
    for entry in _parse_trusted_native_redirect_uris():
        if entry.endswith("*"):
            if _native_wildcard_prefix_matches(normalized, entry[:-1]):
                return True
        elif normalized == entry:
            return True
    return False

