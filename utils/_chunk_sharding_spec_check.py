
def _chunk_sharding_spec_check(spec, op):
    """
    For the given op implementation check if the sharding spec is ChunkShardingSpec.
    """
    if not isinstance(spec, ChunkShardingSpec):
        raise NotImplementedError(
            f"Only ChunkShardingSpec supported for '{op.__name__}'."
        )

