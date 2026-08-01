
def is_tensor_evenly_shardable(shape: Sequence[int], spec: DTensorSpec) -> bool:
    """Check if the shape is evenly shardable according to the spec."""
    # number of shards in each tensor dimension
    num_shards = [1] * len(shape)
    for i, placement in enumerate(spec.placements):
        if _is_shard_like(placement):
            shard_dim = placement.dim
            if shard_dim >= len(shape):
                return False
            num_shards[shard_dim] *= spec.mesh.size(i)
            if isinstance(placement, _StridedShard):
                if (
                    shape[shard_dim] % (placement.split_factor * num_shards[shard_dim])
                    != 0
                ):
                    return False
            else:
                if shape[shard_dim] % num_shards[shard_dim] != 0:
                    return False
    return True

