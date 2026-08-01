
def maybe_enable_local_tracker(
    device_type: str, distribute_region_enabled: bool, spec, generator
):
    """
    Returns a context manager for LocalTensor-mode RNG tracking if local tensor mode is enabled.

    Args:
        device_type: The device type (e.g., "cuda", "cpu")
        distribute_region_enabled: Whether distribute region is enabled
        spec: The DTensorSpec
        generator: Optional torch.Generator

    Returns:
        Context manager from local_tracker._distribute_region if local tensor mode is enabled,
        otherwise None.
    """
    if enabled_local_tensor_mode():
        local_tracker = _LocalOffsetBasedRNGTracker(device_type)
        local_tracker.distribute_region_enabled = distribute_region_enabled
        return local_tracker._distribute_region(spec, generator)

    return None

