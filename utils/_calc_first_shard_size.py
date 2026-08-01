
def _calc_first_shard_size(spec: DTensorSpec) -> list[int]:
    local_size_on_rank_0 = list(spec.shape)
    for idx, placement in enumerate(spec.placements):
        if isinstance(placement, Shard | _StridedShard):
            mesh_dim_size = spec.mesh.size(idx)
            shard_dim = placement.dim
            local_size_on_rank_0[shard_dim], _ = placement._local_shard_size_and_offset(
                spec.shape[shard_dim],
                mesh_dim_size,
                0,
            )
    return local_size_on_rank_0

