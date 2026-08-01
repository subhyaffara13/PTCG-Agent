
def record_csc_network_saved(
    bytes_saved: int,
) -> None:
    """
    Record the number of bytes saved by using Client Side Caching (CSC).

    Args:
        bytes_saved: Number of bytes saved
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_csc_network_saved(
            bytes_saved=bytes_saved,
        )
    except Exception:
        pass

