
def record_connection_count(
    pool_name: str,
    connection_state: ConnectionState,
    counter: int = 1,
) -> None:
    """
    Record a connection count change for a single state.

    Args:
        pool_name: Connection pool identifier
        connection_state: State to update (IDLE or USED)
        counter: Number to add (positive) or subtract (negative)

    Example:
        # New connection created (goes to IDLE first)
        >>> record_connection_count('pool_abc123', ConnectionState.IDLE, 1)

        # Acquire from pool (transition)
        >>> record_connection_count('pool_abc123', ConnectionState.IDLE, -1)
        >>> record_connection_count('pool_abc123', ConnectionState.USED, 1)

        # Release to pool (transition)
        >>> record_connection_count('pool_abc123', ConnectionState.USED, -1)
        >>> record_connection_count('pool_abc123', ConnectionState.IDLE, 1)

        # Pool disconnect 5 idle connections
        >>> record_connection_count('pool_abc123', ConnectionState.IDLE, -5)
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_connection_count(
            pool_name=pool_name,
            connection_state=connection_state,
            counter=counter,
        )
    except Exception:
        pass

