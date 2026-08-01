
def get_observability_instance() -> ObservabilityInstance:
    """
    Get the global observability singleton instance.

    This is the Pythonic way to get the singleton instance.

    Returns:
        The global ObservabilityInstance singleton

    Example:
        >>>
        >>> otel = get_observability_instance()
        >>> otel.init(OTelConfig())
    """
    global _observability_instance

    if _observability_instance is None:
        _observability_instance = ObservabilityInstance()

    return _observability_instance

