
def get_redistribute_planner(
    device_mesh: DeviceMesh,
    dtensor_meta: TensorMeta,
) -> "DTensorRedistributePlanner":
    """
    Factory function to get or create a DTensorRedistributePlanner instance.
    This function provides transparent caching of planner instances based on
    device mesh and dtensor meta. Multiple calls with the same parameters
    will return the same cached instance for better performance.
    Args:
        device_mesh: The device mesh for the planner
        dtensor_meta: TensorMeta of the DTensor to redistribute
    Returns:
        A DTensorRedistributePlanner instance (potentially cached)
    """
    if _are_we_tracing():
        return DTensorRedistributePlanner(device_mesh, dtensor_meta)

    cache_key = (weakref.ref(device_mesh), dtensor_meta)
    if cache_key not in _planner_cache:
        planner = DTensorRedistributePlanner(device_mesh, dtensor_meta)
        _planner_cache[cache_key] = planner

    return _planner_cache[cache_key]

