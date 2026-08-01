
def _create_colwise_spec(
    pg: dist.ProcessGroup | None = None,
) -> ChunkShardingSpec:
    pg_device_type = dist.distributed_c10d._get_pg_default_device(pg).type
    if pg is None:
        placements = [
            f"rank:{idx}/{_gen_rank_device(idx, pg_device_type)}"
            for idx in range(dist.get_world_size())
        ]
    else:
        placements = [
            f"rank:{idx}/{_gen_rank_device(dist.get_global_rank(pg, idx), pg_device_type)}"
            for idx in range(pg.size())
        ]
    return ChunkShardingSpec(
        dim=0,
        placements=cast(list[_remote_device | str], placements),
    )

