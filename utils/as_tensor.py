
def as_tensor(data, dtype=None, device=None):
    if isinstance(data, TensorBox):
        if dtype is not None:
            data = to_dtype(data, dtype)
        if device is not None:
            data = to_device(data, device)
        return data
    return tensor(data, dtype=dtype, device=device)


def as_tensor(g: jit_utils.GraphContext, data, dtype=None, device=None):
    return tensor(g, data, dtype, device)

