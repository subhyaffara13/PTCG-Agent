
def _isconst(x):
    """
    Check if all values in x are the same.  nans are ignored.

    x must be a 1d array.

    The return value is a 1d array with length 1, so it can be used
    in np.apply_along_axis.
    """
    y = x[~np.isnan(x)]
    if y.size == 0:
        return np.array([True])
    else:
        return (y[0] == y).all(keepdims=True)

