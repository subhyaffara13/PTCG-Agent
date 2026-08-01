
def have_same_ndims(tensors: list[Tensor]):
    ndim = tensors[0].ndim
    for tensor in tensors:
        if tensor.ndim != ndim:
            return False
    return True

