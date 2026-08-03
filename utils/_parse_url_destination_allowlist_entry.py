from typing import Optional, Tuple

def _parse_url_destination_allowlist_entry(
    entry: str,
) -> Optional[Tuple[str, Optional[str], Optional[int]]]:
    """Parse an admin allowlist entry into host, optional scheme, optional port.

    Entries may be bare hosts (``api.example.com``), host+port
    (``api.example.com:8443``), or origins (``https://api.example.com``).
    URL paths are intentionally ignored so admins can paste an api_base value.
    """
    entry = entry.strip()
    if not entry:
        return None

    has_scheme = "://" in entry
    parsed = urlparse(entry if has_scheme else f"//{entry}")
    if has_scheme and parsed.scheme not in _ALLOWED_SCHEMES:
        return None
    if parsed.username is not None or parsed.password is not None:
        return None
    if not parsed.hostname:
        return None

    try:
        port = parsed.port
    except ValueError:
        return None

    scheme: Optional[str] = parsed.scheme if has_scheme else None
    if scheme is not None and port is None:
        port = _default_port_for_scheme(scheme)

    return _normalize_host(parsed.hostname), scheme, port

