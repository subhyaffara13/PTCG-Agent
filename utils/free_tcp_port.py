
def free_tcp_port(free_tcp_port_factory: Callable[[], int]) -> int:
    return free_tcp_port_factory()

