
def broadcast_addr(addr):
    """Given the address ntuple returned by ``net_if_addrs()``
    calculates the broadcast address.
    """
    import ipaddress

    if not addr.address or not addr.netmask:
        return None
    if addr.family == socket.AF_INET:
        return str(
            ipaddress.IPv4Network(
                f"{addr.address}/{addr.netmask}", strict=False
            ).broadcast_address
        )
    if addr.family == socket.AF_INET6:
        return str(
            ipaddress.IPv6Network(
                f"{addr.address}/{addr.netmask}", strict=False
            ).broadcast_address
        )

