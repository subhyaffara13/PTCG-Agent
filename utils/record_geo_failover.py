
def record_geo_failover(
    fail_from: "SyncDatabase",
    fail_to: "SyncDatabase",
    reason: GeoFailoverReason,
) -> None:
    """
    Record a geo failover.

    Args:
        fail_from: Database failed from
        fail_to: Database failed to
        reason: Reason for the failover
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_geo_failover(
            fail_from=fail_from,
            fail_to=fail_to,
            reason=reason,
        )
    except Exception:
        pass

