
def _header_value_allowed(
    header_name: str,
    extra_allowlist: Optional[Set[str]] = None,
) -> bool:
    """Return True if this header's value may be forwarded (allowlist, including globs and extra_headers)."""
    lower = header_name.lower()
    if lower in _HEADER_VALUE_ALLOWLIST:
        return True
    for pattern in _HEADER_VALUE_ALLOWLIST:
        if "*" in pattern and fnmatch.fnmatch(lower, pattern):
            return True
    if extra_allowlist and lower in extra_allowlist:
        return True
    return False

