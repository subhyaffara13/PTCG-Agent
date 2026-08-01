
def _addr_tuple_to_ip_address(
    addr: tuple[str, int] | tuple[str, int, int, int],
) -> tuple[ipaddress.IPv4Address, int] | tuple[ipaddress.IPv6Address, int, int, int]:
    """Convert an address tuple to an IPv4Address."""
    return (ipaddress.ip_address(addr[0]), *addr[1:])

