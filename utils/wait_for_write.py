
def wait_for_write(sock: socket.socket, timeout: float | None = None) -> bool:
    """Waits for writing to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, write=True, timeout=timeout)


def wait_for_write(sock: socket.socket, timeout: float | None = None) -> bool:
    """Waits for writing to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, write=True, timeout=timeout)

