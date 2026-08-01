
def normalize_ndarray(arg, parm=None):  # codespell:ignore
    # check the arg is an ndarray, extract its tensor attribute
    if arg is None:
        return arg

    from ._ndarray import ndarray

    if not isinstance(arg, ndarray):
        raise TypeError(f"'{parm.name}' must be an array")  # codespell:ignore
    return arg.tensor

