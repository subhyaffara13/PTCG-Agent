
def get_index_dtype(arrays=(), maxval=None, check_contents=False):
    """
    Based on input (integer) arrays `a`, determine a suitable index data
    type that can hold the data in the arrays.

    Parameters
    ----------
    arrays : tuple of array_like
        Input arrays whose types/contents to check
    maxval : float, optional
        Maximum value needed
    check_contents : bool, optional
        Whether to check the values in the arrays and not just their types.
        Default: False (check only the types)

    Returns
    -------
    dtype : dtype
        Suitable index data type (int32 or int64)

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import sparse
    >>> # select index dtype based on shape
    >>> shape = (3, 3)
    >>> idx_dtype = sparse.get_index_dtype(maxval=max(shape))
    >>> data = [1.1, 3.0, 1.5]
    >>> indices = np.array([0, 1, 0], dtype=idx_dtype)
    >>> indptr = np.array([0, 2, 3, 3], dtype=idx_dtype)
    >>> A = sparse.csr_array((data, indices, indptr), shape=shape)
    >>> A.indptr.dtype
    dtype('int32')

    >>> # select based on larger of existing arrays and shape
    >>> shape = (3, 3)
    >>> idx_dtype = sparse.get_index_dtype(A.indptr, maxval=max(shape))
    >>> idx_dtype
    <class 'numpy.int32'>
    """
    # not using intc directly due to misinteractions with pythran
    if np.intc().itemsize != 4:
        return np.int64

    int32min = np.int32(np.iinfo(np.int32).min)
    int32max = np.int32(np.iinfo(np.int32).max)

    if maxval is not None:
        maxval = np.int64(maxval)
        if maxval > int32max:
            return np.int64

    if isinstance(arrays, np.ndarray):
        arrays = (arrays,)

    for arr in arrays:
        arr = np.asarray(arr)
        if not np.can_cast(arr.dtype, np.int32):
            if check_contents:
                if arr.size == 0:
                    # a bigger type not needed
                    continue
                elif np.issubdtype(arr.dtype, np.integer):
                    maxval = arr.max()
                    minval = arr.min()
                    if minval >= int32min and maxval <= int32max:
                        # a bigger type not needed
                        continue
            return np.int64
    return np.int32

