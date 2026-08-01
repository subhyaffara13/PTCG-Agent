
def add_use_future_nested_cb(to, x, y, z):
    out = torch.futures.Future()

    def callback(fut1):
        fut2 = rpc.rpc_async(to, torch.add, args=(fut1.wait(), z))
        fut2.then(lambda fut2: out.set_result(fut2.wait()))

    fut1 = rpc.rpc_async(to, torch.add, args=(x, y))
    fut1.then(callback)
    return out.wait()

