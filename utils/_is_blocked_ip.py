
def _is_blocked_ip(addr: str) -> bool:
    """Return True for any IP not safe to reach from a user-supplied URL.

    Policy: default-deny via ``ip.is_global`` (RFC 6890), plus an explicit
    exception list for globally-routable cloud-fabric IPs that are still
    dangerous from inside a cloud VM (currently just Azure Wire Server).
    Unparseable addresses fail closed.
    """
    try:
        ip = ip_address(addr)
    except ValueError:
        return True  # fail-closed: unparseable addresses are blocked
    if ip.version == 6 and hasattr(ip, "ipv4_mapped") and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    if not ip.is_global or ip.is_multicast:
        return True
    return any(ip in net for net in _CLOUD_METADATA_EXCEPTIONS)

