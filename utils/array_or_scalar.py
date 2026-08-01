
def array_or_scalar(values, py_type=float, return_scalar=False):
    if return_scalar:
        return py_type(values.item())
    else:
        from ._ndarray import ndarray

        return ndarray(values)

