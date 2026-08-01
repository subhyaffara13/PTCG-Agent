
def bandwidth(a):
    """Return the lower and upper bandwidth of a numeric array.

    Parameters
    ----------
    a : (..., N, M) array_like
        Input array of at least 2 dimensions.

    Returns
    -------
    lower : np.int64 | nDArray[np.int64]
        Lower bandwidth. a scalar ``np.int64`` is assigned per
        2D slice of the input array of last two dimensions. A value of 0
        means the slice is upper triangular; ``N - 1`` means the lower part
        is full. If the input array is 2D then a scalar int64 is returned.
    upper : np.int64 | nDArray[np.int64]
        Upper bandwidth. Same shape rules as `lower`. A value of 0
        means the slice is lower triangular; ``M - 1`` means the upper
        part is full. If the input array is 2D then a scalar int64 is returned.

    Raises
    ------
    TypeError
        If the dtype of the array is not supported, in particular, for NumPy
        float16, float128 and complex256 and other NumPy non-numeric types.

    Notes
    -----
    This helper function simply runs over the array looking for the nonzero
    entries whether there exists a banded structure in the array or not. Hence,
    the performance depends on the density of nonzero entries and also
    memory-layout. Fortran- or C- contiguous arrays are handled best and
    otherwise suffers from extra random memory access cost.

    The strategy is to look for only untested band elements in the upper
    and lower triangular parts separately; depending on the memory layout
    we scan row-wise or column-wise. Moreover, say we are scanning rows
    and in the 6th row, 4th entry is nonzero then, on the succeeding rows
    the horizontal search is done only up to that band entries since we know
    that band is occupied. Therefore, a completely dense matrix scan cost is
    in the order of n.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import bandwidth
    >>> A = np.array([[3., 0., 0., 0., 0.],
    ...               [0., 4., 0., 0., 0.],
    ...               [0., 0., 5., 1., 0.],
    ...               [8., 0., 0., 6., 2.],
    ...               [0., 9., 0., 0., 7.]])
    >>> bandwidth(A)
    (3, 1)

    """
    a = np.asarray(a)
    if a.ndim < 2:
        raise ValueError('Input array must be at least 2D.')

    if np.isdtype(a.dtype, (np.float16, np.longdouble, np.clongdouble)):
        raise TypeError(f'Input array with {a.dtype} dtype is not supported.')

    # Now that the problematic numeric types are tested, test for numeric or bool.
    elif not np.isdtype(a.dtype, ("numeric", "bool")):
        raise TypeError(f'Input array must have a numeric dtype, got {a.dtype}.')

    # Empty array bandwidth is defined to be zero.
    if a.size == 0:
        if a.ndim == 2:
            return (np.int64(0), np.int64(0))

        batch_shape = a.shape[:-2]
        return (
            np.zeros(batch_shape, dtype=np.int64),
            np.zeros(batch_shape, dtype=np.int64)
        )

    return _bandwidth(a)

