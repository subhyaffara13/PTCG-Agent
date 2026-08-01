
def reshuffle_local_shard(
    local_shard: torch.Tensor,
    st_size: torch.Size,
    sharding_spec: shard_spec.ShardingSpec,
    resharding_spec: shard_spec.ShardingSpec,
    pg: ProcessGroup,
) -> tuple[list[Shard], list[ShardMetadata]]:
    """
    Reshuffle the local shard directly when the reshard dim is same as the original
    sharding dim. Logically we do this in two step:
    1. To collect all shards based on original sharding spec.
    2. Reshard the tensor based on the given resharding spec.

    In reality, we consolidate the two steps into one by sending the local tensor to
    the new shard directly based on the resharding spec.

    Args:
        local_shard (Tensor): Local tensor stored in the current rank.
        st_size (torch.Size): The size of the sharded tensor.
        sharding_spec (:class:`torch.distributed._shard.sharding_spec.ShardingSpec`): The
            specification describing how the tensor is sharded originally.
        resharding_spec (:class:`torch.distributed._shard.sharding_spec.ShardingSpec`): The
            specification describing how the tensor will be resharded.
        pg (ProcessGroup): The process group to aggregate on.

    Returns:
        A Tuple of the followings:
            A List[`Shard`] which contains the local tensor and its metadata.
            A List[`ShardMetadata`] which contains the metadata for the shard, including
                offsets, lengths and device placement.
    """
    current_rank = dist.get_rank(pg)
    world_size = dist.get_world_size(pg)
    # Build shards_metadata first.
    shards_metadata, ranks = build_reshard_metadata(
        st_size, resharding_spec, world_size
    )
    # Get input split size for all2all.
    reshard_dim = int(resharding_spec.dim)  # type: ignore[attr-defined]
    split_size = get_split_size(st_size[reshard_dim], world_size)
    input_split_sizes = [0] * world_size
    idx = get_idx_from_placements(sharding_spec.placements, current_rank)  # type: ignore[attr-defined]
    new_rank = resharding_spec.placements[idx].rank()  # type: ignore[union-attr, attr-defined]
    input_split_sizes[new_rank] = local_shard.size(reshard_dim)
    # Get output split size for all2all.
    output_split_sizes = [0] * world_size
    new_idx = ranks.index(current_rank)
    sharded_dim_size = get_chunked_dim_size(st_size[reshard_dim], split_size, new_idx)
    output_split_sizes[new_rank] = sharded_dim_size
    # Get gathered_input for all2all.
    local_shard = local_shard.transpose(0, reshard_dim).contiguous()
    gathered_input_size = list(local_shard.size())
    gathered_input_size[0] = sharded_dim_size
    gathered_input = torch.empty(
        gathered_input_size, device=local_shard.device, dtype=local_shard.dtype
    )
    # all2all.
    local_shard = all_to_all_single(
        gathered_input,
        local_shard,
        input_split_sizes=input_split_sizes,
        output_split_sizes=output_split_sizes,
        group=pg,
    )
    local_tensor = local_shard.transpose(0, reshard_dim).contiguous()
    local_shards = [Shard(local_tensor, shards_metadata[current_rank])]
    return local_shards, shards_metadata

