
def wrap_tensors(result):
    from ._ndarray import ndarray

    if isinstance(result, torch.Tensor):
        return ndarray(result)
    elif isinstance(result, (tuple, list)):
        result = type(result)(wrap_tensors(x) for x in result)
    return result

