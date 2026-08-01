
def async_add_chained_multi(to, x, num, step):
    fut = rpc.rpc_async(to, torch.add, args=(x, 0))
    for _ in range(num):
        fut = fut.then(lambda fut: fut.wait() + step)
    return fut

