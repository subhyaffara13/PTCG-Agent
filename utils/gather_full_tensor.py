
def gather_full_tensor(
    local_tensor: torch.Tensor, shard_dim: int, device_mesh: dist.device_mesh.DeviceMesh
) -> torch.Tensor:
    """
    All-gather a sharded tensor along the specified dimension to reconstruct the full tensor.

    Args:
        local_tensor: The local shard of the tensor on this rank
        shard_dim: The dimension along which the tensor was sharded
        device_mesh: The device mesh for distributed communication

    Returns:
        The full reconstructed tensor (same on all ranks)
    """
    world_size = device_mesh.size()
    # In case of TP+DP configuration, the TP group should be used for gathering, not the full DP group
    process_group = device_mesh.get_group("tp") if "tp" in (device_mesh.mesh_dim_names or {}) else None

    # Normalize negative dimension
    if shard_dim < 0:
        shard_dim = local_tensor.ndim + shard_dim

    # Gather all shards
    gathered_tensors = [torch.empty_like(local_tensor) for _ in range(world_size)]
    dist.all_gather(gathered_tensors, local_tensor.contiguous(), group=process_group)

    # Concatenate along the shard dimension
    return torch.cat(gathered_tensors, dim=shard_dim)

