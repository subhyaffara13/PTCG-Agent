
def _find_all_reduce_mesh_dim(placements: tuple[Placement, ...], dim: int) -> int:
    if not len(placements) == 1:
        raise ValueError(
            "Currently loss_parallel() only supports input on one-dimensional DeviceMesh."
        )
    if not placements[0].is_shard(dim):
        raise ValueError(
            f"loss_parallel() should be enabled only when the input tensor is sharded on dimension {dim}."
        )
    return 0

