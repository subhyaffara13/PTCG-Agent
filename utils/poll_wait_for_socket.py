
def poll_wait_for_socket(
    sock: socket.socket,
    read: bool = False,
    write: bool = False,
    timeout: float | None = None,
) -> bool:
    if not read and not write:
        raise RuntimeError("must specify at least one of read=True, write=True")
    mask = 0
    if read:
        mask |= select.POLLIN
    if write:
        mask |= select.POLLOUT
    poll_obj = select.poll()
    poll_obj.register(sock, mask)

    # For some reason, poll() takes timeout in milliseconds
    def do_poll(t: float | None) -> list[tuple[int, int]]:
        if t is not None:
            t *= 1000
        return poll_obj.poll(t)

    return bool(do_poll(timeout))


def poll_wait_for_socket(
    sock: socket.socket,
    read: bool = False,
    write: bool = False,
    timeout: float | None = None,
) -> bool:
    if not read and not write:
        raise RuntimeError("must specify at least one of read=True, write=True")
    mask = 0
    if read:
        mask |= select.POLLIN
    if write:
        mask |= select.POLLOUT
    poll_obj = select.poll()
    poll_obj.register(sock, mask)

    # For some reason, poll() takes timeout in milliseconds
    def do_poll(t: float | None) -> list[tuple[int, int]]:
        if t is not None:
            t *= 1000
        return poll_obj.poll(t)

    return bool(do_poll(timeout))

