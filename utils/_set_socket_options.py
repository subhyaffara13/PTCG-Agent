
def _set_socket_options(
    sock: socket.socket, options: _TYPE_SOCKET_OPTIONS | None
) -> None:
    if options is None:
        return

    for opt in options:
        sock.setsockopt(*opt)


def _set_socket_options(
    sock: socket.socket, options: _TYPE_SOCKET_OPTIONS | None
) -> None:
    if options is None:
        return

    for opt in options:
        sock.setsockopt(*opt)

