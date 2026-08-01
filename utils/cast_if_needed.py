
def cast_if_needed(tensor, dtype):
    # NB: no casting if dtype=None
    if dtype is not None and tensor.dtype != dtype:
        tensor = tensor.to(dtype)
    return tensor

