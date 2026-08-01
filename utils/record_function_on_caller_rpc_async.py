
def record_function_on_caller_rpc_async(dst_worker_name: str, block: str) -> Tensor:
    t: Tensor = torch.ones(1)
    with record_function(block):
        fut1 = rpc.rpc_async(dst_worker_name, script_add_ones, (t,))
        # Extra operator call to avoid de-duplication of the next async call
        # see https://github.com/pytorch/pytorch/pull/62710#discussion_r694680279
        zero = torch.zeros_like(t)
        fut2 = rpc.rpc_async(dst_worker_name, script_add_ones, (t,))
        res = fut1.wait() + fut2.wait() + zero
    return res

