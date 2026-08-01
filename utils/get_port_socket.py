
def get_port_socket(
    host: str, port: int, family: socket.AddressFamily
) -> socket.socket:
    s = socket.socket(family, socket.SOCK_STREAM)
    if REUSE_ADDRESS:
        # Windows has different semantics for SO_REUSEADDR,
        # so don't set it. Ref:
        # https://docs.microsoft.com/en-us/windows/win32/winsock/using-so-reuseaddr-and-so-exclusiveaddruse
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    return s

