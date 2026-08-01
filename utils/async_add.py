
def async_add(to, x, y):
    return rpc.rpc_async(to, torch.add, args=(x, y))


def async_add(to: str, x: Tensor, y: Tensor) -> Future[Tensor]:
    return rpc.rpc_async(to, script_add, (x, y))

