
def free_tcp_port_factory() -> FreePortFactory:
    return FreePortFactory(socket.SOCK_STREAM)

