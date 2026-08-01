
def record_operation_duration(
    command_name: str,
    duration_seconds: float,
    server_address: Optional[str] = None,
    server_port: Optional[int] = None,
    db_namespace: Optional[str] = None,
    error: Optional[Exception] = None,
    is_blocking: Optional[bool] = None,
    batch_size: Optional[int] = None,  # noqa
    retry_attempts: Optional[int] = None,
) -> None:
    """
    Record a Redis command execution duration.

    This is a simple, clean API that Redis core code can call directly.
    If observability is not enabled, this returns immediately with zero overhead.

    Args:
        command_name: Redis command name (e.g., 'GET', 'SET')
        duration_seconds: Command execution time in seconds
        server_address: Redis server address
        server_port: Redis server port
        db_namespace: Redis database index
        error: Exception if command failed, None if successful
        is_blocking: Whether the operation is a blocking command
        batch_size: Number of commands in batch (for pipelines/transactions)
        retry_attempts: Number of retry attempts made

    Example:
        >>> start = time.monotonic()
        >>> # ... execute command ...
        >>> record_operation_duration('SET', time.monotonic() - start, 'localhost', 6379, '0')
    """
    global _metrics_collector

    # Fast path: if collector not initialized, observability is disabled
    if _metrics_collector is None:
        # Try to initialize (only once)
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return  # Observability not enabled

    # Record the metric
    try:
        _metrics_collector.record_operation_duration(
            command_name=command_name,
            duration_seconds=duration_seconds,
            server_address=server_address,
            server_port=server_port,
            db_namespace=db_namespace,
            error_type=error,
            network_peer_address=server_address,
            network_peer_port=server_port,
            is_blocking=is_blocking,
            retry_attempts=retry_attempts,
        )
    except Exception:
        # Don't let metric recording errors break Redis operations
        pass

