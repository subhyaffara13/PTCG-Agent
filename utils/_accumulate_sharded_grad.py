
def _accumulate_sharded_grad(
    state: _FSDPState,
    handle: FlatParamHandle,
    sharded_grad: torch.Tensor,
) -> torch.Tensor:
    """
    Accumulates the reduce-scattered sharded gradient with any existing sharded
    gradient if needed, returning the gradient to offload (if CPU offloading is
    enabled).
    """
    flat_param = handle.flat_param
    _cast_grad_to_param_dtype(state, sharded_grad, flat_param)
    # Save the sharded gradient in `_saved_grad_shard` to support gradient
    # accumulation -- for multiple backwards, the gradient reductions may
    # happen in arbitrary order
    accumulate_grad = hasattr(flat_param, "_saved_grad_shard")
    if accumulate_grad:
        _check_grad_to_accumulate(sharded_grad, flat_param._saved_grad_shard)
        flat_param._saved_grad_shard += sharded_grad
    else:
        flat_param._saved_grad_shard = sharded_grad
    grad_to_offload = flat_param._saved_grad_shard
    return grad_to_offload

