
def _shard_tensor(
    full_tensor: torch.Tensor,
    placements: Sequence[Shard],
    device_mesh: DeviceMesh | None = None,
) -> "DTensor":
    """
    Locally shards a full tensor based on indicated sharding arrangement, and
    returns a DTensor containing the local shard.

    .. warning:: This is a private API that is subject to change. It skips the
        communication otherwise required by `distribute_tensor`. It is only
        applicable to cases where all ranks have the same `full_tensor`. For
        example, in distributed inference all ranks load from the same
        checkpoint. This API will not check for data equality between ranks, it
        is thus user's responsibility to ensure the `full_tensor` is the same
        across ranks.

    Args:
        full_tensor (torch.Tensor): the full tensor to be sharded.
        placements (Sequence[:class:`Shard`]): the placements that
            describes how to place the local tensor on DeviceMesh.
        device_mesh (:class:`DeviceMesh`, optional): DeviceMesh to place the
            DTensor.  Must have same dimension as the number of placements.
            If not specified, would be retrieve from current context.

    Returns:
        A :class:`DTensor` object with the shard as its local tensor.

    Examples:
        >>> # xdoctest: +SKIP("need world_size and rank")
        >>> device_mesh = dist.init_device_mesh("cuda", (world_size,))
        >>> full_tensor = torch.arange(world_size, device=f"cuda:{rank}")
        >>> dtensor = _shard_tensor(full_tensor, [Shard(1)], device_mesh)
    """
    return distribute_tensor(full_tensor, device_mesh, placements, src_data_rank=None)


def _shard_tensor(
    tensor: torch.Tensor, sharding_spec: ShardingSpec, src_rank=0, process_group=None
) -> ShardedTensor:
    """
    Given a :class:`torch.Tensor`, it shards that tensor according to the provided
    ``sharding_spec``. ``src_rank`` denotes the source rank which would be
    used as the ground truth of the data which would be scattered as shards
    across the rest of the ranks.

    Args:
        tensor (:class:`torch.Tensor`): Tensor needs to be sharded.
        sharding_spec (:class:`torch.distributed._shard.sharding_spec.ShardingSpec`): The specification
            describing how to shard the Tensor.

    Keyword args:
        src_rank (int, optional): The source rank which is used as the ground truth of
            the data for the parameter that would be sharded and scattered
            across the rest of the ranks.
            Default: 0.
        process_group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.

    Returns:
        A :class:`ShardedTensor` sharded from the given tensor.

    .. warning::
        Only :class:`torch.distributed._shard.sharding_spec.ChunkShardingSpec` is
        currently supported as the ``sharding_spec``.
    """
    if not tensor.is_contiguous():
        raise ValueError("input tensor is not a contiguous Tensor")

    pg = (
        process_group
        if process_group is not None
        else distributed_c10d._get_default_group()
    )
    world_size = dist.get_world_size(pg)
    current_rank = dist.get_rank(pg)

    # Validate src_rank and sharding_spec are same across all ranks.
    gathered_list = [None] * world_size
    dist.all_gather_object(gathered_list, (src_rank, sharding_spec), group=pg)

    for idx, entry in enumerate(gathered_list):
        if src_rank != entry[0]:  # type: ignore[index]
            raise ValueError(
                f"src_rank={src_rank} on rank: {current_rank} does not "  # type: ignore[index]
                f"match with src_rank={entry[0]} on rank: {idx}"  # type: ignore[index]
            )
        if sharding_spec != entry[1]:  # type: ignore[index]
            raise ValueError(
                f"sharding_spec={sharding_spec} on rank: {current_rank} does not "  # type: ignore[index]
                f"match with sharding_spec={entry[1]} on rank: {idx}"  # type: ignore[index]
            )

    st = sharding_spec.shard(tensor, src_rank=src_rank, process_group=pg)

    return st

