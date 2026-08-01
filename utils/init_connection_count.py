
def init_connection_count() -> None:
    """
    Initialize observable gauge for connection count metric.
    """
    collector = _get_or_create_collector()
    if collector is None:
        return

    def observable_callback(__):
        observables_registry = get_observables_registry_instance()
        callbacks = observables_registry.get(CONNECTION_COUNT_REGISTRY_KEY)
        observations = []

        for callback in callbacks:
            observations.extend(callback())

        return observations

    try:
        collector.init_connection_count(
            callback=observable_callback,
        )
    except Exception:
        pass

