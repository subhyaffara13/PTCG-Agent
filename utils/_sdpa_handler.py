from typing import Callable

def _sdpa_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    # extract local tensor and sharding infos to a OpInfo
    op_info = DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)
    logger.debug("Dispatching op_call: %s", op_info.schema or op_call)

    # sharding propagation
    # TODO: remove the context parallel strategy from the default propagation
    # rule. Either figure out how to dynamically enable it or just don't call
    # propagate.
    DTensor._op_dispatcher.sharding_propagator.propagate(op_info)
    output_sharding = op_info.output_sharding
    if output_sharding is None:
        raise AssertionError("output sharding should not be None")
    if output_sharding.needs_redistribute:
        raise AssertionError("inputs need to be redistributed")

    call_maps: dict[torch._ops.OpOverload, Callable] = {
        aten._scaled_dot_product_flash_attention.default: _scaled_dot_product_ring_flash_attention,
        aten._scaled_dot_product_efficient_attention.default: _scaled_dot_product_ring_efficient_attention,
        aten._scaled_dot_product_cudnn_attention.default: _scaled_dot_product_ring_cudnn_attention,
        aten._scaled_dot_product_flash_attention_backward.default: _scaled_dot_product_ring_flash_attention_backward,
        aten._scaled_dot_product_efficient_attention_backward.default: _scaled_dot_product_ring_efficient_attention_backward,
        aten._scaled_dot_product_cudnn_attention_backward.default: _scaled_dot_product_ring_cudnn_attention_backward,
    }
    if op_call in call_maps:
        local_results = call_maps[op_call](
            op_info.compute_mesh,
            *op_info.local_args,  # type: ignore[arg-type]
            **op_info.local_kwargs,  # type: ignore[arg-type]
        )
    else:
        raise NotImplementedError(
            "CP only supports flash attention and memory efficient attention now."
        )

    return DTensor._op_dispatcher.wrap(local_results, output_sharding.output_spec)

