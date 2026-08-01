
def rpc_async_call_with_timeout(
    dst_worker_name: str,
    args: tuple[Tensor, Tensor],
    kwargs: dict[str, Tensor],
    timeout: float,
):
    fut = rpc.rpc_async(dst_worker_name, two_args_two_kwargs, args, kwargs, timeout)
    ret = fut.wait()
    return ret

