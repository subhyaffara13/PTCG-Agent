
def as_series(request):
    """
    Boolean fixture to support arr and Series(arr) comparison testing.
    """
    return request.param


def as_series(alist, trim=True):
    """
    Return argument as a list of 1-d arrays.

    The returned list contains array(s) of dtype double, complex double, or
    object.  A 1-d argument of shape ``(N,)`` is parsed into ``N`` arrays of
    size one; a 2-d argument of shape ``(M,N)`` is parsed into ``M`` arrays
    of size ``N`` (i.e., is "parsed by row"); and a higher dimensional array
    raises a Value Error if it is not first reshaped into either a 1-d or 2-d
    array.

    Parameters
    ----------
    alist : array_like
        A 1- or 2-d array_like
    trim : boolean, optional
        When True, trailing zeros are removed from the inputs.
        When False, the inputs are passed through intact.

    Returns
    -------
    [a1, a2,...] : list of 1-D arrays
        A copy of the input data as a list of 1-d arrays.

    Raises
    ------
    ValueError
        Raised when `as_series` cannot convert its input to 1-d arrays, or at
        least one of the resulting arrays is empty.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.polynomial import polyutils as pu
    >>> a = np.arange(4)
    >>> pu.as_series(a)
    [array([0.]), array([1.]), array([2.]), array([3.])]
    >>> b = np.arange(6).reshape((2,3))
    >>> pu.as_series(b)
    [array([0., 1., 2.]), array([3., 4., 5.])]

    >>> pu.as_series((1, np.arange(3), np.arange(2, dtype=np.float16)))
    [array([1.]), array([0., 1., 2.]), array([0., 1.])]

    >>> pu.as_series([2, [1.1, 0.]])
    [array([2.]), array([1.1])]

    >>> pu.as_series([2, [1.1, 0.]], trim=False)
    [array([2.]), array([1.1, 0. ])]

    """
    arrays = [np.array(a, ndmin=1, copy=None) for a in alist]
    for a in arrays:
        if a.size == 0:
            raise ValueError("Coefficient array is empty")
        if a.ndim != 1:
            raise ValueError("Coefficient array is not 1-d")
    if trim:
        arrays = [trimseq(a) for a in arrays]

    try:
        dtype = np.common_type(*arrays)
    except Exception as e:
        object_dtype = np.dtypes.ObjectDType()
        has_one_object_type = False
        ret = []
        for a in arrays:
            if a.dtype != object_dtype:
                tmp = np.empty(len(a), dtype=object_dtype)
                tmp[:] = a[:]
                ret.append(tmp)
            else:
                has_one_object_type = True
                ret.append(a.copy())
        if not has_one_object_type:
            raise ValueError("Coefficient arrays have no common type") from e
    else:
        ret = [np.array(a, copy=True, dtype=dtype) for a in arrays]
    return ret

