
def find_free_port():
    """
    Finds an available port and returns that port number.

    NOTE: If this function is being used to allocate a port to Store (or
    indirectly via init_process_group or init_rpc), it should be used
    in conjunction with the `retry_on_connect_failures` decorator as there is a potential
    race condition where the allocated port may become unavailable before it can be used
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 0))
        _, port = sock.getsockname()
        return port


def find_free_port():
    """
    Find a free port and binds a temporary socket to it so that the port can be "reserved" until used.

    .. note:: the returned socket must be closed before using the port,
              otherwise a ``address already in use`` error will happen.
              The socket should be held and closed as close to the
              consumer of the port as possible since otherwise, there
              is a greater chance of race-condition where a different
              process may see the port as being free and take it.

    Returns: a socket binded to the reserved free port

    Usage::

    sock = find_free_port()
    port = sock.getsockname()[1]
    sock.close()
    use_port(port)
    """
    addrs = socket.getaddrinfo(
        host="localhost", port=None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM
    )

    for addr in addrs:
        family, type, proto, _, _ = addr
        try:
            s = socket.socket(family, type, proto)
            s.bind(("localhost", 0))
            s.listen(0)
            return s
        except OSError as e:
            s.close()  # type: ignore[possibly-undefined]
            print(f"Socket creation attempt failed: {e}")
    raise RuntimeError("Failed to create a socket")


def find_free_port():
  with contextlib.closing(
      socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ) as s:
    s.bind(("", 0))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s.getsockname()[1]

