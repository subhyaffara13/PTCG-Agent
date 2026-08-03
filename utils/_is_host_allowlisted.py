from typing import List, Set

def _is_host_allowlisted(hostname: str, effective_port: int) -> bool:
    """Check whether a host is in the admin-configured allowlist.

    Admin entries may be ``hostname`` (any port) or ``hostname:port``. IPv6
    literals are written bracketed (``[::1]`` / ``[::1]:8080``). Matching
    is case-insensitive on the hostname.
    """
    configured: List[str] = getattr(litellm, "user_url_allowed_hosts", []) or []
    if not configured:
        return False
    normalized_host = _normalize_host(hostname)
    host_repr = f"[{normalized_host}]" if ":" in normalized_host else normalized_host
    candidates: Set[str] = {host_repr, f"{host_repr}:{effective_port}"}
    allowlist: Set[str] = {_normalize_host(entry) for entry in configured if entry}
    return bool(candidates & allowlist)

