
def create_healthcheck_server(
    alive_callback: Callable[[], int],
    port: int,
    timeout: int,
) -> HealthCheckServer:
    """
    creates health check server object
    """
    return HealthCheckServer(alive_callback, port, timeout)

