
def get_observables_registry_instance() -> ObservablesRegistry:
    """
    Get the global observables registry singleton instance.

    This is the Pythonic way to get the singleton instance.

    Returns:
        The global ObservablesRegistry singleton

    Example:
        >>>
        >>> registry = get_observables_registry_instance()
        >>> registry.register('my_metric', my_callback)
    """
    global _observables_registry_instance

    if _observables_registry_instance is None:
        _observables_registry_instance = ObservablesRegistry()

    return _observables_registry_instance

