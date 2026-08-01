
def _fix_shape_1d(x, n, axis):
    if n < 1:
        raise ValueError(
            f"invalid number of data points ({n}) specified")

    return _fix_shape(x, (n,), (axis,))

