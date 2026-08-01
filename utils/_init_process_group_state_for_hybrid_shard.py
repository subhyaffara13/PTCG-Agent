
def _init_process_group_state_for_hybrid_shard(
    state: _FSDPState,
    process_group: ProcessGroupType,
    device_mesh: DeviceMesh,
) -> _FSDPState:
    if device_mesh:
        if _is_valid_hybrid_shard_device_mesh(device_mesh):
            state._device_mesh = device_mesh
            # We currently only allow _inter_node_pg to be the outermost dimension, and the
            # process_group(intra_node) to be the innermost dimension.
            state._inter_node_pg = device_mesh.get_group(mesh_dim=0)
            state.process_group = device_mesh.get_group(mesh_dim=1)
        else:
            raise ValueError(
                f"Expected device_mesh to have ndim=2 but got {device_mesh.ndim}"
            )
    elif process_group is None:
        default_group = _get_default_group()
        intra_node_group, inter_node_group = _init_intra_and_inter_node_groups(
            default_group, state._device_handle.device_count()
        )
        # we shard across intra-node
        state.process_group = intra_node_group
        # save _inter_node_pg to allreduce across.
        state._inter_node_pg = inter_node_group
    else:
        # Check type and assign state.process_group and state._inter_node_pg.
        if _is_valid_hybrid_shard_pg_type(process_group):
            # Assuming that user passed in as intra node group and inter node group
            # as documented.
            state.process_group, state._inter_node_pg = process_group
        else:
            raise ValueError(
                "Expected process_group to be passed in as either None or "
                f"Tuple[dist.ProcessGroup, dist.ProcessGroup] but got {type(process_group)}"
            )
    # Create state for allreduce
    state._inter_node_state = _get_default_comm_hook_state(
        process_group=state._inter_node_pg,
    )
    return state

