
def record_connection_closed(
    close_reason: Optional[CloseReason] = None,
    error_type: Optional[Exception] = None,
) -> None:
    """
    Record a connection closed event.

    Args:
        close_reason: Reason for closing (e.g. 'error', 'application_close')
        error_type: Error type if closed due to error

    Example:
        >>> record_connection_closed('ConnectionPool<localhost:6379>', 'idle_timeout')
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_connection_closed(
            close_reason=close_reason,
            error_type=error_type,
        )
    except Exception:
        pass

