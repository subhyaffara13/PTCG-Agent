
def get_unused_port_socket(
    host: str, family: socket.AddressFamily = socket.AF_INET
) -> socket.socket:
    return get_port_socket(host, 0, family)

