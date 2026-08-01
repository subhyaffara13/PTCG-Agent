
def free_udp_port_factory() -> FreePortFactory:
    return FreePortFactory(socket.SOCK_DGRAM)

