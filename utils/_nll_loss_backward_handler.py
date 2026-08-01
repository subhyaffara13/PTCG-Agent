
def _nll_loss_backward_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    grad_output = cast(DTensor, args[0])
    x = cast(DTensor, args[1])
    target = args[2]
    weight = args[3]
    reduction = cast(int, args[4])
    ignore_index = cast(int, args[5])
    total_weight = cast(Tensor, args[6])

    channel_dim = 1 if x.dim() >= 2 else 0
    spec = x._spec
    mesh_dim = _find_all_reduce_mesh_dim(spec.placements, channel_dim)

    # if target and weight are not DTensors, convert them to DTensors
    target_placements = _skip_dim(
        replicate_reduction_dims(spec.placements, [channel_dim]), channel_dim
    )
    all_replicate_placements = (Replicate(),) * spec.mesh.ndim
    target = _cast_to_dtensor(target, target_placements, spec.mesh)
    if weight is not None:
        weight = _cast_to_dtensor(weight, all_replicate_placements, spec.mesh)

    # tensor inputs to _propagate_tensor_meta need to be DTensors
    # pyrefly: ignore [bad-assignment]
    args = list(args)
    # pyrefly: ignore [unsupported-operation]
    args[2], args[3] = target, weight
    # pyrefly: ignore [unsupported-operation]
    args[6] = _cast_to_dtensor(total_weight, all_replicate_placements, spec.mesh)
    output_tensor_meta = _propagate_tensor_meta(op_call, tuple(args), kwargs)

    result = _nll_loss_and_log_softmax_backward(
        grad_output._local_tensor,
        x._local_tensor,
        target._local_tensor,
        weight._local_tensor if weight is not None else None,
        reduction,
        ignore_index,
        total_weight,
        x.shape,
        channel_dim,
        spec.mesh,
        mesh_dim,
    )
    # the output sharding is the same as input sharding: Shard(channel_dim) on mesh_dim
    out_spec = DTensorSpec(
        spec.mesh,
        spec.placements,
        tensor_meta=output_tensor_meta,
    )

    # pyrefly: ignore [bad-argument-type]
    return DTensor(
        # pyrefly: ignore [bad-argument-count]
        result,
        out_spec,
        # pyrefly: ignore [unexpected-keyword]
        requires_grad=result.requires_grad,
    )

