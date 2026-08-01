
def create_barrier_from_config(
    barrier_config: BarrierConfig,
) -> Optional["Barrier"]:
    """
    Create a barrier instance from BarrierConfig.

    Args:
        barrier_config: Configuration for barrier construction.

    Returns:
        Barrier instance or None if no barrier type is configured.

    Raises:
        ValueError: If the barrier_type is not found in the registry.
    """
    if barrier_config.barrier_type is None:
        return None

    if barrier_config.barrier_type not in BARRIER_REGISTRY:
        raise ValueError(
            f"Unknown barrier type: {barrier_config.barrier_type}. "
            f"Available types: {list(BARRIER_REGISTRY.keys())}"
        )

    barrier_class = BARRIER_REGISTRY[barrier_config.barrier_type]
    return barrier_class(**barrier_config.barrier_args)

