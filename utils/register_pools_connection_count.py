
def register_pools_connection_count(
    connection_pools: List["ConnectionPoolInterface"],
) -> None:
    """
    Add connection pools to connection count observable registry.
    """
    collector = _get_or_create_collector()
    if collector is None:
        return

    try:
        # Lazy import
        from opentelemetry.metrics import Observation

        def connection_count_callback():
            observations = []
            for connection_pool in connection_pools:
                for count, attributes in connection_pool.get_connection_count():
                    observations.append(Observation(count, attributes=attributes))
            return observations

        observables_registry = get_observables_registry_instance()
        observables_registry.register(
            CONNECTION_COUNT_REGISTRY_KEY, connection_count_callback
        )
    except Exception:
        pass

