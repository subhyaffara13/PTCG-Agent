
def reset_observability_instance() -> None:
    """
    Reset the global observability singleton instance.

    This is primarily used for testing and benchmarking to ensure
    a clean state between test runs.

    Warning:
        This will shutdown any active provider manager and reset
        the global state. Use with caution in production code.
    """
    global _observability_instance

    if _observability_instance is not None:
        _observability_instance.shutdown()
        _observability_instance = None

