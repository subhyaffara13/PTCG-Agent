from typing import List

def is_url_destination_allowed_by_host(url: str, allowed_hosts: List[str]) -> bool:
    """Return True when a credential-bearing provider URL is admin-allowlisted.

    This does not fetch, resolve, or rewrite URLs. It only answers whether the
    destination origin is explicitly trusted by configuration. Use ``safe_get``
    for user-controlled content fetches that require SSRF protection.
    """
    parsed = urlparse(url)
    if parsed.scheme not in _ALLOWED_SCHEMES:
        return False
    if parsed.username is not None or parsed.password is not None:
        return False
    if not parsed.hostname:
        return False

    try:
        effective_port = parsed.port or _default_port_for_scheme(parsed.scheme)
    except ValueError:
        return False

    normalized_host = _normalize_host(parsed.hostname)
    configured_entries = (
        [allowed_hosts] if isinstance(allowed_hosts, str) else allowed_hosts
    )
    for entry in configured_entries or []:
        if not isinstance(entry, str):
            continue
        parsed_entry = _parse_url_destination_allowlist_entry(entry)
        if parsed_entry is None:
            continue
        allowed_host, allowed_scheme, allowed_port = parsed_entry
        if allowed_host != normalized_host:
            continue
        if allowed_scheme is not None and allowed_scheme != parsed.scheme:
            continue
        if allowed_port is not None and allowed_port != effective_port:
            continue
        return True
    return False

