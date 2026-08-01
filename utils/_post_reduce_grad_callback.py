
def _post_reduce_grad_callback(
    state: _FSDPState,
    handle: FlatParamHandle,
    # Additional arguments needed for the callback logic
    grad_to_offload: torch.Tensor,
):
    """
    This callback captures any logic to run after the gradient reduction
    finishes. Currently, this offloads the gradient to CPU if CPU offloading is
    enabled and uses sharded gradient views if ``use_orig_params=True``.
    """
    _offload_grad(state, handle, grad_to_offload)
    _post_backward_use_sharded_grad_views(handle)

