
def _init_intra_and_inter_node_groups(
    global_process_group: dist.ProcessGroup,
    num_devices_per_node: int,
) -> tuple[dist.ProcessGroup, dist.ProcessGroup]:
    """
    Initialize intra and inter-node process groups and return the ones corresponding to this process's rank.

    This function can be used to initialize process groups for ``HYBRID_SHARD`` or
    ``_HYBRID_SHARD_ZERO2`` in FSDP.
    This function assumes each node has an equal number of CUDA-enabled devices.
    Returns:
        Tuple[dist.ProcessGroup, dist.ProcessGroup]: Intra and inter-node process group.
    """
    return (
        _init_intra_node_process_group(num_devices_per_node),
        _init_inter_node_process_group(global_process_group, num_devices_per_node),
    )

