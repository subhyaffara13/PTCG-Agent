from typing import Optional

def record_csc_request(
    result: Optional[CSCResult] = None,
):
    """
    Record a Client Side Caching (CSC) request.

    Args:
        result: CSC result ('hit' or 'miss')
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    try:
        _metrics_collector.record_csc_request(
            result=result,
        )
    except Exception:
        pass

