
def _gather_tensors(
    gather_dim: int,
    gathered_idxs: torch.Tensor,
    local_redux: torch.Tensor,
    device_mesh: "torch.distributed.device_mesh.DeviceMesh",
    shard_mesh_dims: list[int],
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Gather the min or max of the tensors and their corresponding indices.

    Args:
        gather_dim: The dim to stack the collected min/max tensors.
        gathered_idxs: The local tensor holding the corresponding indices.
        local_redux: The local tensor holding the operator's value i.e. min/max.
        device_mesh: Device mesh of the DTensor.
        shard_mesh_dims: List of mesh dimensions that are sharded.

    Returns:
        All gathered tensors (gathered_redux, gathered_idxs) of the reducing operator.
    """
    gathered_redux = local_redux
    for mesh_dim in shard_mesh_dims:
        gathered_redux = funcol.all_gather_tensor(
            gathered_redux,
            gather_dim=gather_dim,
            group=(device_mesh, mesh_dim),
        )
        gathered_idxs = funcol.all_gather_tensor(
            gathered_idxs,
            gather_dim=gather_dim,
            group=(device_mesh, mesh_dim),
        )
    return gathered_redux, gathered_idxs

