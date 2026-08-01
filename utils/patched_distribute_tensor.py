
def patched_distribute_tensor(
    input_tensor,
    device_mesh,
    placements,
    shard_order,
    use_graph_based_transform=True,
    src_data_rank: int | None = 0,
):
    """wrapper function to support shard_order for tensor distribution"""
    if placements is None:
        placements = shard_order_to_placement(shard_order, device_mesh)
    placements = tuple(placements)
    tensor_dt = distribute_tensor(
        input_tensor, device_mesh, placements, src_data_rank=src_data_rank
    )
    # Do not consider _StridedShard to express shard order
    tensor_dt._spec.use_strided_shard_as_shard_order = False
    tensor_dt._spec.__post_init__()
    # fix the shard order
    return redistribute(
        tensor_dt, device_mesh, placements, shard_order, use_graph_based_transform
    )

