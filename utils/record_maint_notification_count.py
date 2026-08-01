
def record_maint_notification_count(
    server_address: str,
    server_port: int,
    network_peer_address: str,
    network_peer_port: int,
    maint_notification: str,
) -> None:
    """
    Record a maintenance notification count.

    Args:
        server_address: Server address
        server_port: Server port
        network_peer_address: Network peer address
        network_peer_port: Network peer port
        maint_notification: Maintenance notification type (e.g., 'MOVING', 'MIGRATING')

    Example:
        >>> record_maint_notification_count('localhost', 6379, 'localhost', 6379, 'MOVING')
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_maint_notification_count(
            server_address=server_address,
            server_port=server_port,
            network_peer_address=network_peer_address,
            network_peer_port=network_peer_port,
            maint_notification=maint_notification,
        )
    except Exception:
        pass

