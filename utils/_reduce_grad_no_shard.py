
def _reduce_grad_no_shard(state: _FSDPState, handle: FlatParamHandle) -> None:
    """
    For no-shard, this runs gradient reduction (which directly covers any
    gradient accumulation implicitly) and the post-reduction callback.
    """
    flat_param = handle.flat_param
    if state._comm_hook is None:  # default path
        _div_if_needed(flat_param.grad, state._gradient_predivide_factor)
        dist.all_reduce(flat_param.grad, group=state.process_group)
        _div_if_needed(flat_param.grad, state._gradient_postdivide_factor)
    else:
        state._comm_hook(state._comm_hook_state, flat_param.grad)
    # For `NO_SHARD`, we can keep the low precision gradients by simply
    # omitting the cast altogether
    if not handle._keep_low_precision_grads:
        _cast_grad_to_param_dtype(state, flat_param.grad, flat_param)
    grad_to_offload = flat_param.grad.data
    _post_reduce_grad_callback(state, handle, grad_to_offload)

