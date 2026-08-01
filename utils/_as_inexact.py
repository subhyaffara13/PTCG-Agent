
def _as_inexact(x):
    """Return `x` as an array, of either floats or complex floats"""
    x = asarray(x)
    if not np.issubdtype(x.dtype, np.inexact):
        return asarray(x, dtype=np.float64)
    return x

