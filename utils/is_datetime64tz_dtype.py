
def is_datetime64tz_dtype(arr_or_dtype) -> bool:
    """
    Check whether an array-like or dtype is of a DatetimeTZDtype dtype.

    .. deprecated:: 2.1.0
        Use isinstance(dtype, pd.DatetimeTZDtype) instead.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array-like or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array-like or dtype is of a DatetimeTZDtype dtype.

    See Also
    --------
    api.types.is_datetime64_dtype: Check whether an array-like or
                                        dtype is of the datetime64 dtype.
    api.types.is_datetime64_any_dtype: Check whether the provided array or
                                        dtype is of the datetime64 dtype.

    Examples
    --------
    >>> from pandas.api.types import is_datetime64tz_dtype
    >>> is_datetime64tz_dtype(object)
    False
    >>> is_datetime64tz_dtype([1, 2, 3])
    False
    >>> is_datetime64tz_dtype(pd.DatetimeIndex([1, 2, 3]))  # tz-naive
    False
    >>> is_datetime64tz_dtype(pd.DatetimeIndex([1, 2, 3], tz="US/Eastern"))
    True

    >>> from pandas import DatetimeTZDtype
    >>> dtype = DatetimeTZDtype("ns", tz="US/Eastern")
    >>> s = pd.Series([], dtype=dtype)
    >>> is_datetime64tz_dtype(dtype)
    True
    >>> is_datetime64tz_dtype(s)
    True
    """
    # GH#52607
    warnings.warn(
        "is_datetime64tz_dtype is deprecated and will be removed in a future "
        "version. Check `isinstance(dtype, pd.DatetimeTZDtype)` instead.",
        Pandas4Warning,
        stacklevel=2,
    )
    if isinstance(arr_or_dtype, DatetimeTZDtype):
        # GH#33400 fastpath for dtype object
        # GH 34986
        return True

    if arr_or_dtype is None:
        return False
    return DatetimeTZDtype.is_dtype(arr_or_dtype)

