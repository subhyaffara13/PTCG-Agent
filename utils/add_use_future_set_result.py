
def add_use_future_set_result(to, x, y, z):
    out = torch.futures.Future()
    fut = rpc.rpc_async(to, torch.add, args=(x, y))
    fut.then(lambda fut: out.set_result(fut.wait() + z))
    return out.wait()

