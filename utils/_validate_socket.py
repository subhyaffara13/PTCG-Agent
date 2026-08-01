
def _validate_socket(
    sock_or_fd: socket.socket | int,
    sock_type: socket.SocketKind,
    addr_family: socket.AddressFamily = socket.AF_UNSPEC,
    *,
    require_connected: bool = False,
    require_bound: bool = False,
) -> socket.socket:
    if isinstance(sock_or_fd, int):
        try:
            sock = socket.socket(fileno=sock_or_fd)
        except OSError as exc:
            if exc.errno == errno.ENOTSOCK:
                raise ValueError(
                    "the file descriptor does not refer to a socket"
                ) from exc
            elif require_connected:
                raise ValueError("the socket must be connected") from exc
            elif require_bound:
                raise ValueError("the socket must be bound to a local address") from exc
            else:
                raise
    elif isinstance(sock_or_fd, socket.socket):
        sock = sock_or_fd
    else:
        raise TypeError(
            f"expected an int or socket, got {type(sock_or_fd).__qualname__} instead"
        )

    try:
        if require_connected:
            try:
                sock.getpeername()
            except OSError as exc:
                raise ValueError("the socket must be connected") from exc

        if require_bound:
            try:
                if sock.family in (socket.AF_INET, socket.AF_INET6):
                    bound_addr = sock.getsockname()[1]
                else:
                    bound_addr = sock.getsockname()
            except OSError:
                bound_addr = None

            if not bound_addr:
                raise ValueError("the socket must be bound to a local address")

        if addr_family != socket.AF_UNSPEC and sock.family != addr_family:
            raise ValueError(
                f"address family mismatch: expected {addr_family.name}, got "
                f"{sock.family.name}"
            )

        if sock.type != sock_type:
            raise ValueError(
                f"socket type mismatch: expected {sock_type.name}, got {sock.type.name}"
            )
    except BaseException:
        # Avoid ResourceWarning from the locally constructed socket object
        if isinstance(sock_or_fd, int):
            sock.detach()

        raise

    sock.setblocking(False)
    return sock

