
def spawn_materialize(
    thread_pool: ThreadPoolExecutor | None,
    tensor: torch.Tensor,
    device=None,
    dtype=None,
) -> Future | Callable:
    """Materialize a tensor from file asynchronously if `thread_pool` is provided, or return a Callable that will
    load the tensor synchronously when called."""

    def _job():
        return _materialize_copy(tensor, device, dtype)

    if thread_pool is not None:
        return thread_pool.submit(_job)
    else:
        # Return the Callable here, not the Tensor itself, so we actually delay loading to avoid saturating cpu
        # memory during Conversion
        return _job

