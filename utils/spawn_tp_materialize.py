
def spawn_tp_materialize(
    thread_pool: ThreadPoolExecutor | None, tensor: torch.Tensor, sharding_method, tensor_idx, device=None, dtype=None
) -> Future | Callable:
    """Materialize and shard a tensor (according to the TP-plan) from file asynchronously if `thread_pool` is provided, or
    return a Callable that will load the tensor synchronously when called."""

    def _job():
        return sharding_method.shard_tensor(tensor, tensor_idx=tensor_idx, device=device, dtype=dtype)

    if thread_pool is not None:
        return thread_pool.submit(_job)
    else:
        # Return the Callable here, not the Tensor itself, so we actually delay loading to avoid saturating cpu
        # memory during Conversion
        return _job

