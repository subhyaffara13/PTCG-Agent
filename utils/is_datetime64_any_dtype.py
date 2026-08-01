
def is_datetime64_any_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of the datetime64 dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array or dtype to check.

    Returns
    -------
    bool
        Whether or not the array or dtype is of the datetime64 dtype.

    See Also
    --------
    api.types.is_datetime64_dtype : Check whether an array-like or dtype is of the
        datetime64 dtype.
    api.is_datetime64_ns_dtype : Check whether the provided array or dtype is of the
        datetime64[ns] dtype.
    api.is_datetime64tz_dtype : Check whether an array-like or dtype is of a
        DatetimeTZDtype dtype.

    Examples
    --------
    >>> from pandas.api.types import is_datetime64_any_dtype
    >>> from pandas.api.types import DatetimeTZDtype
    >>> is_datetime64_any_dtype(str)
    False
    >>> is_datetime64_any_dtype(int)
    False
    >>> is_datetime64_any_dtype(np.datetime64)  # can be tz-naive
    True
    >>> is_datetime64_any_dtype(DatetimeTZDtype("ns", "US/Eastern"))
    True
    >>> is_datetime64_any_dtype(np.array(["a", "b"]))
    False
    >>> is_datetime64_any_dtype(np.array([1, 2]))
    False
    >>> is_datetime64_any_dtype(np.array([], dtype="datetime64[ns]"))
    True
    >>> is_datetime64_any_dtype(pd.DatetimeIndex([1, 2, 3], dtype="datetime64[ns]"))
    True
    """
    if isinstance(arr_or_dtype, (np.dtype, ExtensionDtype)):
        # GH#33400 fastpath for dtype object
        return arr_or_dtype.kind == "M"

    if arr_or_dtype is None:
        return False

    try:
        tipo = _get_dtype(arr_or_dtype)
    except TypeError:
        return False
    return (
        lib.is_np_dtype(tipo, "M")
        or isinstance(tipo, DatetimeTZDtype)
        or (isinstance(tipo, ExtensionDtype) and tipo.kind == "M")
    )

