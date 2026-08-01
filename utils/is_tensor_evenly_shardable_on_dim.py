
def is_tensor_evenly_shardable_on_dim(
    shape: Sequence[int], spec: DTensorSpec, dim: int
) -> bool:
    """Check if the shape is evenly shardable according to the spec on dim."""
    dim = normalize_dim(dim, len(shape))

    num_shards = 1
    for i, placement in enumerate(spec.placements):
        if _is_shard_like(placement) and placement.dim == dim:
            num_shards *= spec.mesh.size(i)
            if isinstance(placement, _StridedShard):
                # _StridedShard._split_tensor first chunks into split_factor
                # groups, then into num_shards within each group, so the dim
                # must be divisible by the product of both.  This is stricter
                # than the final num_shards check and implies it.  Note:
                # num_shards already includes spec.mesh.size(i) from this
                # iteration, so the check covers the full shard count.
                if shape[dim] % (placement.split_factor * num_shards) != 0:
                    return False

    return shape[dim] % num_shards == 0

