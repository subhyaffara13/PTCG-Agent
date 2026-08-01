
def addr_to_addr_infos(
    addr: tuple[str, int, int, int] | tuple[str, int, int] | tuple[str, int] | None,
) -> list[AddrInfoType] | None:
    """Convert an address tuple to a list of addr_info tuples."""
    if addr is None:
        return None
    host = addr[0]
    port = addr[1]
    is_ipv6 = ":" in host
    if is_ipv6:
        flowinfo = 0
        scopeid = 0
        addr_len = len(addr)
        if addr_len >= 4:
            scopeid = addr[3]  # type: ignore[misc]
        if addr_len >= 3:
            flowinfo = addr[2]  # type: ignore[misc]
        addr = (host, port, flowinfo, scopeid)
        family = socket.AF_INET6
    else:
        addr = (host, port)
        family = socket.AF_INET
    return [(family, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", addr)]

