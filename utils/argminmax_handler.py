
def argminmax_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    """
    Handler for aten.argmin.default and aten.argmax.default ops.

    This is a pure function handler that doesn't require instantiation.
    """
    if op_call not in _ARGMINMAX_REDUCTION_OPS:
        raise NotImplementedError(f"Unsupported reduction op: {op_call}")

    local_tensor, global_shape, device_mesh, placements, dim, keepdim = _prep_arguments(
        str(op_call), args, kwargs
    )
    output_sharding = _get_output_sharding(op_call, args, kwargs)

    expected_shape = _get_expected_shape(local_tensor, dim, keepdim)
    shard_mesh_dims = _collect_shard_mesh_dims(
        str(op_call), local_tensor, placements, dim
    )

    # Compute local reduction
    if dim is None:
        val_op = _ARGMINMAX_REDUCTION_OPS[op_call]
        # unsqueeze scalars to 1-d so they can be allgathered
        local_redux = val_op(local_tensor).unsqueeze(0)
        local_idx = op_call(local_tensor).unsqueeze(0)
    else:
        val_op = _ARGMINMAX_REDUCTION_OPS[op_call]
        local_redux, local_idx = val_op(local_tensor, dim=dim, keepdim=True)

    if not shard_mesh_dims:
        return dtensor.DTensor._op_dispatcher.wrap(
            local_idx.reshape(expected_shape), output_sharding.output_spec
        )

    gather_dim, gathered_idxs = _convert_to_global_idxs(
        local_idx, global_shape, device_mesh, placements, dim
    )
    gathered_redux, gather_idxs = _gather_tensors(
        gather_dim, gathered_idxs, local_redux, device_mesh, shard_mesh_dims
    )
    # Select the rank with the best value; use dim=0 when dim was None since
    # the scalars were unsqueezed to 1-d for gathering
    select_dim = 0 if dim is None else dim
    rank_winner = op_call(gathered_redux, select_dim, True)
    final_idx = torch.gather(gather_idxs, dim=gather_dim, index=rank_winner)

    return dtensor.DTensor._op_dispatcher.wrap(
        final_idx.reshape(expected_shape), output_sharding.output_spec
    )

