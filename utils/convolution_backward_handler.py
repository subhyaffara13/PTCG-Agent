
def convolution_backward_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    # Redistribute grad_output tensor to the same placement as input tensor
    # pyrefly: ignore [bad-assignment]
    args = list(args)
    if not (
        isinstance(args[0], dtensor.DTensor) and isinstance(args[1], dtensor.DTensor)
    ):
        raise AssertionError
    # pyrefly: ignore [unsupported-operation]
    args[0] = args[0].redistribute(args[1].device_mesh, args[1].placements)
    args = tuple(args)

    # extract local tensor and sharding infos to a OpInfo
    op_info = dtensor.DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)

    # sharding propagation
    dtensor.DTensor._op_dispatcher.sharding_propagator.propagate(op_info)
    output_sharding = op_info.output_sharding
    if output_sharding is None:
        raise AssertionError("output sharding should not be None")
    if not isinstance(op_info.flat_args_schema[0], dtensor.DTensorSpec):
        raise AssertionError

    # local propagation
    local_results = tp_convolution_backward(
        op_call,
        tuple(op_info.local_args),
        op_info.local_kwargs,
        op_info.flat_args_schema[0].dim_map,
    )

    return dtensor.DTensor._op_dispatcher.wrap(
        local_results, output_sharding.output_spec
    )

