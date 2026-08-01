
def is_timedelta64_dtype(arr_or_dtype) -> bool:
    """
    Check whether an array-like or dtype is of the timedelta64 dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array-like or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array-like or dtype is of the timedelta64 dtype.

    See Also
    --------
    api.types.is_timedelta64_ns_dtype : Check whether the provided array or dtype is
        of the timedelta64[ns] dtype.
    api.types.is_period_dtype : Check whether an array-like or dtype is of the
        Period dtype.

    Examples
    --------
    >>> from pandas.api.types import is_timedelta64_dtype
    >>> is_timedelta64_dtype(object)
    False
    >>> is_timedelta64_dtype(np.timedelta64)
    True
    >>> is_timedelta64_dtype([1, 2, 3])
    False
    >>> is_timedelta64_dtype(pd.Series([], dtype="timedelta64[ns]"))
    True
    >>> is_timedelta64_dtype("0 days")
    False
    """
    if isinstance(arr_or_dtype, np.dtype):
        # GH#33400 fastpath for dtype object
        return arr_or_dtype.kind == "m"

    return _is_dtype_type(arr_or_dtype, classes(np.timedelta64))

