
def normalize_axis_like(arg, parm=None):  # codespell:ignore
    from ._ndarray import ndarray

    if isinstance(arg, ndarray):
        arg = operator.index(arg)
    return arg

