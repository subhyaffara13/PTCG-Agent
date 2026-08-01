
def _quantile_bc(y, p, n, method, xp):
    # Methods retained for backward compatibility. NumPy documentation is not
    # quite right about what these methods do: if `p * (n - 1)` is integral,
    # that is used as the index. See numpy/numpy#28910.
    ij = p * (n - 1)
    if method == '_midpoint':
        return (xp.take_along_axis(y, xp.astype(xp.floor(ij), xp.int64), axis=-1)
                + xp.take_along_axis(y, xp.astype(xp.ceil(ij), xp.int64), axis=-1)) / 2
    elif method == '_lower':
        k = xp.floor(ij)
    elif method == '_higher':
        k = xp.ceil(ij)
    elif method == '_nearest':
        k = xp.round(ij)
    return xp.take_along_axis(y, xp.astype(k, xp.int64), axis=-1)

