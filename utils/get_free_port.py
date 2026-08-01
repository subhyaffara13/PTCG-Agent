
def get_free_port():
    """
    Returns an unused port on localhost.

    This function finds an unused port on localhost by opening to socket to bind
    to a port and then closing it.

    Returns:
        int: an unused port on localhost

    Example:
        >>> # xdoctest: +SKIP("Nondeterministic")
        >>> get_free_port()
        63976

    .. note::
        The port returned by :func:`get_free_port` is not reserved and may be
        taken by another process after this function returns.
    """
    sock = get_socket_with_port()
    with closing(sock):
        return sock.getsockname()[1]

