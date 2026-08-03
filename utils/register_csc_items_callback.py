from typing import Callable, Optional

def register_csc_items_callback(
    callback: Callable,
    pool_name: Optional[str] = None,
) -> None:
    """
    Adds given callback to CSC items observable registry.

    Args:
        callback: Callback function that returns the cache size
        pool_name: Connection pool name for observability
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    # Lazy import
    from opentelemetry.metrics import Observation

    def csc_items_callback():
        return [
            Observation(
                callback(),
                attributes=AttributeBuilder.build_csc_attributes(pool_name=pool_name),
            )
        ]

    try:
        observables_registry = get_observables_registry_instance()
        observables_registry.register(CSC_ITEMS_REGISTRY_KEY, csc_items_callback)
    except Exception:
        pass

