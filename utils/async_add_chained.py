
def async_add_chained(to, x, y, z):
    return rpc.rpc_async(to, torch.add, args=(x, y)).then(lambda fut: fut.wait() + z)

