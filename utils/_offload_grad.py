
def _offload_grad(
    state: _FSDPState,
    handle: FlatParamHandle,
    grad_to_offload: torch.Tensor,
):
    if not handle._offload_params:
        return
    # Offload the gradient to CPU to ensure parameters and gradients are on the
    # same device as required by the optimizer
    # TODO: Investigate why `NO_SHARD` breaks correctness when using
    # `non_blocking=True` here.
    # TODO (rohan-varma): When CPU offload and optimizer overlap,
    # non_blocking=True won't work since the copy may have not finished before
    # the optimizer step executes on CPU. If we want to use non-blocking=True
    # here, we'll have to synchronize before using result on CPU.
    non_blocking = handle.uses_sharded_strategy and not handle._has_optim_in_backward
    handle.flat_param._cpu_grad.copy_(
        grad_to_offload.detach(), non_blocking=non_blocking
    )  # synchronized in the post-backward callback
    # Since the gradient being offloaded may have been produced in the
    # computation stream and is being consumed here in the post-backward
    # stream, inform the caching allocator
    _no_dispatch_record_stream(grad_to_offload.data, state._post_backward_stream)

