
def _parse_trusted_redirect_origins() -> List[str]:
    """Parse ``MCP_TRUSTED_REDIRECT_ORIGINS`` into normalized entries.
    Empty / unset env var → empty list. Entries are lowercased and any
    scheme / path component the operator included is stripped. Default
    ``:443`` is also stripped from non-wildcard entries so
    ``app.example.com:443`` matches a redirect_netloc whose own ``:443``
    has already been normalized away — the allowlist path is https-only,
    so ``:443`` is the only default port that can legitimately appear.
    """
    raw = os.environ.get(_TRUSTED_REDIRECT_ORIGINS_ENV, "").strip()
    if not raw:
        return []
    entries: List[str] = []
    for token in raw.split(","):
        entry = token.strip().lower()
        if not entry:
            continue
        if "://" in entry:
            entry = entry.split("://", 1)[1]
        entry = entry.split("/", 1)[0]
        if not entry:
            continue
        # Wildcards don't express port constraints; leave them alone.
        if not entry.startswith("*."):
            entry = _strip_default_port("https", entry)
        if entry:
            entries.append(entry)
    return entries

