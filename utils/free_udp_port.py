from typing import Callable

def free_udp_port(free_udp_port_factory: Callable[[], int]) -> int:
    return free_udp_port_factory()

