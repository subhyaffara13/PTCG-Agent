
def record_connection_create_time(
    connection_pool: "ConnectionPoolInterface",
    duration_seconds: float,
) -> None:
    """
    Record connection creation time.

    Args:
        connection_pool: Connection pool implementation
        duration_seconds: Time taken to create connection in seconds

    Example:
        >>> start = time.monotonic()
        >>> # ... create connection ...
        >>> record_connection_create_time('ConnectionPool<localhost:6379>', time.monotonic() - start)
    """
    global _metrics_collector

    # Fast path: if collector not initialized, observability is disabled
    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_connection_create_time(
            connection_pool=connection_pool,
            duration_seconds=duration_seconds,
        )
    except Exception:
        pass

