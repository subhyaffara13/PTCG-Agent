from typing import Optional

def record_error_count(
    server_address: Optional[str] = None,
    server_port: Optional[int] = None,
    network_peer_address: Optional[str] = None,
    network_peer_port: Optional[int] = None,
    error_type: Optional[Exception] = None,
    retry_attempts: Optional[int] = None,
    is_internal: bool = True,
) -> None:
    """
    Record error count.

    Args:
        server_address: Server address
        server_port: Server port
        network_peer_address: Network peer address
        network_peer_port: Network peer port
        error_type: Error type (Exception)
        retry_attempts: Retry attempts
        is_internal: Whether the error is internal (e.g., timeout, network error)

    Example:
        >>> record_error_count('localhost', 6379, 'localhost', 6379, ConnectionError(), 3)
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_error_count(
            server_address=server_address,
            server_port=server_port,
            network_peer_address=network_peer_address,
            network_peer_port=network_peer_port,
            error_type=error_type,
            retry_attempts=retry_attempts,
            is_internal=is_internal,
        )
    except Exception:
        pass

