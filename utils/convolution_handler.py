
def convolution_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    # extract local tensor and sharding infos to a OpInfo
    op_info = dtensor.DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)

    # sharding propagation
    dtensor.DTensor._op_dispatcher.sharding_propagator.propagate(op_info)
    output_sharding = op_info.output_sharding
    if output_sharding is None:
        raise AssertionError("output sharding should not be None")
    output_spec = output_sharding.output_spec
    if not isinstance(output_spec, dtensor.DTensorSpec):
        raise AssertionError

    # local propagation
    local_results = tp_convolution(
        op_call,
        tuple(op_info.local_args),
        op_info.local_kwargs,
        output_spec.dim_map,
    )

    return dtensor.DTensor._op_dispatcher.wrap(local_results, output_spec)

