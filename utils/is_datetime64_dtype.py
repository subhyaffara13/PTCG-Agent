
def is_datetime64_dtype(arr_or_dtype) -> bool:
    """
    Check whether an array-like or dtype is of the datetime64 dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array-like or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array-like or dtype is of the datetime64 dtype.

    See Also
    --------
    api.types.is_datetime64_ns_dtype: Check whether the provided array or
                                        dtype is of the datetime64[ns] dtype.
    api.types.is_datetime64_any_dtype: Check whether the provided array or
                                        dtype is of the datetime64 dtype.

    Examples
    --------
    >>> from pandas.api.types import is_datetime64_dtype
    >>> is_datetime64_dtype(object)
    False
    >>> is_datetime64_dtype(np.datetime64)
    True
    >>> is_datetime64_dtype(np.array([], dtype=int))
    False
    >>> is_datetime64_dtype(np.array([], dtype=np.datetime64))
    True
    >>> is_datetime64_dtype([1, 2, 3])
    False
    """
    if isinstance(arr_or_dtype, np.dtype):
        # GH#33400 fastpath for dtype object
        return arr_or_dtype.kind == "M"
    return _is_dtype_type(arr_or_dtype, classes(np.datetime64))

