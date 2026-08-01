
def rpc_async_with_rref_arg(dst_worker_name: str, args: tuple[RRef[Tensor]]) -> Tensor:
    fut = rpc.rpc_async(dst_worker_name, rref_to_here, args)
    ret = fut.wait()
    return ret

