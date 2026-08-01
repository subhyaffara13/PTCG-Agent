
def is_ip_address(host: str | None) -> bool:
    """Check if host looks like an IP Address.

    This check is only meant as a heuristic to ensure that
    a host is not a domain name.
    """
    if not host:
        return False
    # For a host to be an ipv4 address, it must be all numeric.
    # The host must contain a colon to be an IPv6 address.
    return ":" in host or host.replace(".", "").isdigit()

