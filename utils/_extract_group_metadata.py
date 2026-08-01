
def _extract_group_metadata(target_pg: ProcessGroup) -> dict:
    """Extract metadata from the original group before cleanup."""
    original_backend_name, original_store = _world.pg_map[target_pg]
    original_backend_config = _world.pg_backend_config.get(target_pg, "")
    original_group_name = _get_process_group_name(target_pg)

    # Extract device binding information before cleanup to avoid accessing destroyed group
    bound_device_id = None
    if hasattr(target_pg, "bound_device_id"):
        bound_device_id = target_pg.bound_device_id

    # Generate new group name for the shrunk group; hash for uniqueness across backends
    remaining_ranks = list(get_process_group_ranks(target_pg))
    new_group_name = _process_group_name(remaining_ranks, use_hashed_name=True)

    return {
        "backend_name": original_backend_name,
        "store": original_store,
        "backend_config": original_backend_config,
        "original_group_name": original_group_name,
        "new_group_name": new_group_name,
        "bound_device_id": bound_device_id,  # Safe to access after cleanup
    }

