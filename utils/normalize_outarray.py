
def normalize_outarray(arg, parm=None):  # codespell:ignore
    # almost normalize_ndarray, only return the array, not its tensor
    if arg is None:
        return arg
    from ._ndarray import ndarray

    # Dynamo can pass torch tensors as out arguments,
    # wrap it in an ndarray before processing
    if isinstance(arg, torch.Tensor):
        arg = ndarray(arg)

    if not isinstance(arg, ndarray):
        raise TypeError(f"'{parm.name}' must be an array")  # codespell:ignore
    return arg

