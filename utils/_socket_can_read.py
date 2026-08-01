
def _socket_can_read(sock, timeout: float) -> bool:
    # SSL sockets can have decrypted bytes buffered above the OS socket layer.
    if hasattr(sock, "pending") and sock.pending():
        return True
    # timeout=0 must be a non-blocking readiness check only; both branches
    # below are non-destructive and have no FD_SETSIZE limit (select.select
    # raises ValueError for fds >= 1024).
    if _HAS_POLL:
        # Prefer poll() over selectors.DefaultSelector: epoll/kqueue selectors
        # allocate a file descriptor per check and so fail with EMFILE under
        # fd exhaustion - the very condition that pushes sockets onto high
        # fds. poll() allocates nothing.
        poller = select.poll()
        poller.register(sock, select.POLLIN)
        # poll() takes milliseconds (None blocks forever). POLLHUP/POLLERR/
        # POLLNVAL are always reported regardless of the registered mask, so
        # closed or errored sockets still count as readable, like select().
        poll_timeout = None if timeout is None else timeout * 1000
        return bool(poller.poll(poll_timeout))
    with selectors.DefaultSelector() as selector:
        selector.register(sock, selectors.EVENT_READ)
        return bool(selector.select(timeout))

