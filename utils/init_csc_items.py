
def init_csc_items() -> None:
    """
    Initialize observable gauge for CSC items metric.
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    def observable_callback(__):
        observables_registry = get_observables_registry_instance()
        callbacks = observables_registry.get(CSC_ITEMS_REGISTRY_KEY)
        observations = []

        for callback in callbacks:
            observations.extend(callback())

        return observations

    try:
        _metrics_collector.init_csc_items(
            callback=observable_callback,
        )
    except Exception:
        pass

