
def _get_array(shape, dtype):
    """
    Get a test array of given shape and data type.
    Returned NxN matrices are posdef, and 2xN are banded-posdef.

    """
    if len(shape) == 2 and shape[0] == 2:
        # yield a banded positive definite one
        x = np.zeros(shape, dtype=dtype)
        x[0, 1:] = -1
        x[1] = 2
        return x
    elif len(shape) == 2 and shape[0] == shape[1]:
        # always yield a positive definite matrix
        x = np.zeros(shape, dtype=dtype)
        j = np.arange(shape[0])
        x[j, j] = 2
        x[j[:-1], j[:-1]+1] = -1
        x[j[:-1]+1, j[:-1]] = -1
        return x
    else:
        np.random.seed(1234)
        return np.random.randn(*shape).astype(dtype)

