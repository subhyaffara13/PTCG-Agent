
def _collect_shard_mesh_dims(
    op_call_repr: str,
    local_tensor: torch.Tensor,
    placements: tuple[Placement, ...],
    dim: int | None,
) -> list[int]:
    """Collect mesh dimensions that are sharded along the reduction dimension."""
    shard_mesh_dims: list[int] = []
    for mesh_dim, p in enumerate(placements):
        if isinstance(p, Shard):
            if dim is None or p.dim == (dim if dim >= 0 else local_tensor.ndim + dim):
                shard_mesh_dims.append(mesh_dim)
        elif isinstance(p, _StridedShard):
            raise NotImplementedError(f"{op_call_repr} does not support _StridedShard!")
    return shard_mesh_dims

