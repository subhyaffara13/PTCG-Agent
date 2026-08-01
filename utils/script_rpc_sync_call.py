
def script_rpc_sync_call(
    dst_worker_name: str, args: tuple[Tensor, Tensor], kwargs: dict[str, Tensor]
):
    res = rpc.rpc_sync(dst_worker_name, two_args_two_kwargs, args, kwargs)
    return res

