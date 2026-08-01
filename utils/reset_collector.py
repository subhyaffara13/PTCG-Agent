
def reset_collector() -> None:
    """
    Reset the global collector (used for testing or re-initialization).
    """
    global _metrics_collector
    _metrics_collector = None


def reset_collector() -> None:
    """
    Reset the global async collector (used for testing or re-initialization).
    """
    global _async_metrics_collector
    _async_metrics_collector = None

