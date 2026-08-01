
def slow_async_add(to, x, y, device="cpu"):
    return rpc.rpc_async(to, slow_add, args=(x, y, device))

