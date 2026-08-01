
def _native_wildcard_prefix_matches(normalized: str, prefix: str) -> bool:
    """Prefix match for ``entry*`` allowlist rows.

    When the prefix does not end with ``/``, only exact matches or
    deeper path segments (``prefix/...``) are accepted — not siblings
    like ``prefix-2``.
    """
    if not normalized.startswith(prefix):
        return False
    suffix = normalized[len(prefix) :]
    if not suffix:
        return True
    if prefix.endswith("/"):
        return True
    return suffix[0] == "/"

