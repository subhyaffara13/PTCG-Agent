import copy

def redistribute(
    dtensor_input,
    device_mesh,
    placements,
    shard_order,
    use_graph_based_transform=True,
):
    """
    wrapper function to support shard_order for redistribution
    This is a simpler version of Redistribute, only considers the forward.
    """
    if placements is None:
        placements = shard_order_to_placement(shard_order, device_mesh)
    placements = tuple(placements)
    old_spec = dtensor_input._spec
    new_spec = copy.deepcopy(old_spec)
    new_spec.placements = placements
    if shard_order is not None:
        new_spec.shard_order = shard_order
    else:
        new_spec.shard_order = ()
    if old_spec == new_spec:
        return dtensor_input
    dtensor_input = DTensor.from_local(
        redistribute_local_tensor(
            dtensor_input.to_local(),
            old_spec,
            new_spec,
            use_graph_based_transform=use_graph_based_transform,
        ),
        device_mesh,
    )
    dtensor_input._spec = copy.deepcopy(new_spec)
    return dtensor_input  # returns DTensor

