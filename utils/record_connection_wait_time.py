
def record_connection_wait_time(
    pool_name: str,
    duration_seconds: float,
) -> None:
    """
    Record time taken to obtain a connection from the pool.

    Args:
        pool_name: Connection pool identifier
        duration_seconds: Wait time in seconds

    Example:
        >>> start = time.monotonic()
        >>> # ... wait for connection from pool ...
        >>> record_connection_wait_time('ConnectionPool<localhost:6379>', time.monotonic() - start)
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_connection_wait_time(
            pool_name=pool_name,
            duration_seconds=duration_seconds,
        )
    except Exception:
        pass

