
def minmax_dim_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    """
    Handler for aten.min.dim and aten.max.dim ops.

    This is a pure function handler that doesn't require instantiation.
    """
    local_tensor, global_shape, device_mesh, placements, dim, keepdim = _prep_arguments(
        str(op_call), args, kwargs
    )
    output_sharding = _get_output_sharding(op_call, args, kwargs)

    expected_shape = _get_expected_shape(local_tensor, dim, keepdim)
    shard_mesh_dims = _collect_shard_mesh_dims(
        str(op_call), local_tensor, placements, dim
    )

    # Compute local reduction - min/max with dim always requires dim
    if dim is None:
        raise AssertionError
    local_redux, local_idx = op_call(local_tensor, dim=dim, keepdim=True)

    if not shard_mesh_dims:
        return dtensor.DTensor._op_dispatcher.wrap(
            (
                local_redux.reshape(expected_shape),
                local_idx.reshape(expected_shape),
            ),
            output_sharding.output_spec,
        )

    gather_dim, gathered_idxs = _convert_to_global_idxs(
        local_idx, global_shape, device_mesh, placements, dim
    )

    gathered_redux, gather_idxs = _gather_tensors(
        gather_dim, gathered_idxs, local_redux, device_mesh, shard_mesh_dims
    )
    # The op_call here is min/max with dim which returns (values, indices)
    final_redux, rank_winner = op_call(gathered_redux, dim, True)
    final_idx = torch.gather(gather_idxs, dim=gather_dim, index=rank_winner)

    return dtensor.DTensor._op_dispatcher.wrap(
        (
            final_redux.reshape(expected_shape),
            final_idx.reshape(expected_shape),
        ),
        output_sharding.output_spec,
    )

