
def _build_aiohttp_keepalive_socket_factory() -> (
    Optional[Callable[[Tuple[Any, ...]], socket.socket]]
):
    """
    Build a socket_factory that enables SO_KEEPALIVE on aiohttp TCP sockets.

    Why: by default, aiohttp creates sockets without SO_KEEPALIVE, so the kernel
    sends nothing during a long idle TCP connection. NAT/LB hops (e.g. AWS NAT
    Gateway, 350s idle timeout) reap the flow well before slow provider
    responses (OpenAI/Azure: up to 600s) arrive. Enabling SO_KEEPALIVE makes
    the kernel emit TCP probes that reset the NAT idle timer.

    Returns None when AIOHTTP_SO_KEEPALIVE is disabled or aiohttp is too old.
    """
    if not AIOHTTP_SO_KEEPALIVE or not _AIOHTTP_SUPPORTS_SOCKET_FACTORY:
        return None

    def factory(addr_info: Tuple[Any, ...]) -> socket.socket:
        family, type_, proto = addr_info[0], addr_info[1], addr_info[2]
        sock = socket.socket(family=family, type=type_, proto=proto)
        sock.setblocking(False)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # Linux: TCP_KEEPIDLE is idle-before-first-probe.
        # macOS/Darwin: TCP_KEEPALIVE is the equivalent.
        if hasattr(socket, "TCP_KEEPIDLE"):
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, AIOHTTP_TCP_KEEPIDLE
            )
        elif hasattr(socket, "TCP_KEEPALIVE"):
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, AIOHTTP_TCP_KEEPIDLE
            )
        if hasattr(socket, "TCP_KEEPINTVL"):
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, AIOHTTP_TCP_KEEPINTVL
            )
        if hasattr(socket, "TCP_KEEPCNT"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, AIOHTTP_TCP_KEEPCNT)
        return sock

    return factory

