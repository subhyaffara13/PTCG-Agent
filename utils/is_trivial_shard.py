
def is_trivial_shard(p: Placement, tensor_shape: tuple[int, ...]) -> bool:
    """Check if placement is a Shard on a size-1 dimension."""
    # NOTE: isinstance(_, Shard) does not match _StridedShard; see _is_shard_like().
    return (
        isinstance(p, Shard) and p.dim < len(tensor_shape) and tensor_shape[p.dim] == 1
    )

