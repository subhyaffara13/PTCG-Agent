
def _create_shrunk_process_group(
    new_backend, remaining_ranks: list[int], metadata: dict, is_default_group: bool
) -> ProcessGroup:
    """Create and configure the new shrunk process group."""
    # Create new group properties
    new_group_rank = new_backend.rank()
    new_group_size = new_backend.size()
    group_name = metadata["new_group_name"]

    # Generate descriptive group description
    if is_default_group:
        group_desc = "default:shrunken"
    else:
        group_desc = f"{metadata['original_group_name']}:shrunk"

    # Create process group with new communicator (clone the parent store like split does)
    prefix_store = PrefixStore(f"{group_name}/", metadata["store"].clone())
    new_pg = ProcessGroup(prefix_store, new_group_rank, new_group_size)

    # Configure backend using the device type of the new backend's bound device if available,
    # otherwise derive from the original group's bound device or fall back to CPU.
    backend_device = metadata.get("bound_device_id")
    if backend_device is None:
        # Default to CPU if no bound device is present
        backend_device = torch.device("cpu")

    # Choose backend enum based on device type
    if backend_device.type == "cuda":
        backend_type = ProcessGroup.BackendType.NCCL
    else:
        backend_type = ProcessGroup.BackendType.GLOO

    new_pg._register_backend(backend_device, backend_type, new_backend)
    new_pg._set_default_backend(backend_type)

    # Inherit device binding from original group if it was bound
    bound_device_id = metadata.get("bound_device_id")
    if bound_device_id is not None:
        new_pg.bound_device_id = bound_device_id

    # Set group metadata
    new_pg._set_group_name(group_name)
    new_pg._set_group_desc(group_desc)

    # Persist backend configuration overrides (if provided via shrink_group)
    backend_config_override = metadata.get("backend_config")
    if backend_config_override is not None:
        # Store for introspection/debugging and potential backend hooks
        _world.pg_backend_config[new_pg] = backend_config_override

    return new_pg

