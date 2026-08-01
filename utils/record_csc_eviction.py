
def record_csc_eviction(
    count: int,
    reason: Optional[CSCReason] = None,
) -> None:
    """
    Record a Client Side Caching (CSC) eviction.

    Args:
        count: Number of evictions
        reason: Reason for eviction
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_csc_eviction(
            count=count,
            reason=reason,
        )
    except Exception:
        pass

