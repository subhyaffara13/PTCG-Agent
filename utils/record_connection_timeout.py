
def record_connection_timeout(
    pool_name: str,
) -> None:
    """
    Record a connection timeout event.

    Args:
        pool_name: Connection pool identifier

    Example:
        >>> record_connection_timeout('ConnectionPool<localhost:6379>')
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_connection_timeout(
            pool_name=pool_name,
        )
    except Exception:
        pass

