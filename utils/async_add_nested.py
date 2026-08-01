
def async_add_nested(to, x, y, z):
    return rpc.rpc_async(to, async_add, args=(to, x, y)).then(
        lambda fut: fut.wait() + z
    )

