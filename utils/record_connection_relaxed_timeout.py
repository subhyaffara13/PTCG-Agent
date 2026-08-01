
def record_connection_relaxed_timeout(
    connection_name: str,
    maint_notification: str,
    relaxed: bool,
) -> None:
    """
    Record a connection timeout relaxation event.

    Args:
        connection_name: Connection identifier
        maint_notification: Maintenance notification type
        relaxed: True to count up (relaxed), False to count down (unrelaxed)

    Example:
        >>> record_connection_relaxed_timeout('localhost:6379_a1b2c3d4', 'MOVING', True)
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_connection_relaxed_timeout(
            connection_name=connection_name,
            maint_notification=maint_notification,
            relaxed=relaxed,
        )
    except Exception:
        pass

