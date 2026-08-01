
def found_inf_reduce_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> None:
    op_info = dtensor.DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)
    local_tensor_args = pytree.tree_unflatten(
        cast(list[object], op_info.local_args),
        op_info.args_tree_spec,  # type: ignore[arg-type]
    )
    local_tensor_args = cast(tuple[object, ...], local_tensor_args)
    op_call(*local_tensor_args, **op_info.local_kwargs)

    grad_dtensor = cast(list[dtensor.DTensor], args[0])[0]
    grad_placements = grad_dtensor.placements
    mesh = grad_dtensor.device_mesh

    found_inf_placements: list[Placement] = []
    for placement in grad_placements:
        if isinstance(placement, Replicate):
            found_inf_placements.append(placement)
        else:
            found_inf_placements.append(Partial("max"))

    target_tensor = cast(torch.Tensor, args[1])
    spec = DTensorSpec(
        mesh=mesh,
        placements=tuple(found_inf_placements),
        tensor_meta=TensorMeta(
            shape=target_tensor.size(),
            stride=target_tensor.stride(),
            dtype=target_tensor.dtype,
        ),
    )
    # pyrefly: ignore [bad-argument-type]
    found_inf_dtensor = dtensor.DTensor(
        local_tensor=target_tensor,  # pyrefly: ignore [unexpected-keyword]
        spec=spec,  # pyrefly: ignore [unexpected-keyword]
        requires_grad=False,  # pyrefly: ignore [unexpected-keyword]
    )
    found_inf = found_inf_dtensor.full_tensor()
    target_tensor.copy_(found_inf)

