
def is_datetime64_ns_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of the datetime64[ns] dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array or dtype to check.

    Returns
    -------
    bool
        Whether or not the array or dtype is of the datetime64[ns] dtype.

    See Also
    --------
    api.types.is_datetime64_dtype: Check whether an array-like or
                                        dtype is of the datetime64 dtype.
    api.types.is_datetime64_any_dtype: Check whether the provided array or
                                        dtype is of the datetime64 dtype.

    Examples
    --------
    >>> from pandas.api.types import is_datetime64_ns_dtype
    >>> from pandas.api.types import DatetimeTZDtype
    >>> is_datetime64_ns_dtype(str)
    False
    >>> is_datetime64_ns_dtype(int)
    False
    >>> is_datetime64_ns_dtype(np.datetime64)  # no unit
    False
    >>> is_datetime64_ns_dtype(DatetimeTZDtype("ns", "US/Eastern"))
    True
    >>> is_datetime64_ns_dtype(np.array(["a", "b"]))
    False
    >>> is_datetime64_ns_dtype(np.array([1, 2]))
    False
    >>> is_datetime64_ns_dtype(np.array([], dtype="datetime64"))  # no unit
    False
    >>> is_datetime64_ns_dtype(np.array([], dtype="datetime64[ps]"))  # wrong unit
    False
    >>> is_datetime64_ns_dtype(pd.DatetimeIndex([1, 2, 3], dtype="datetime64[ns]"))
    True
    """
    if arr_or_dtype is None:
        return False
    try:
        tipo = _get_dtype(arr_or_dtype)
    except TypeError:
        return False
    return tipo == DT64NS_DTYPE or (
        isinstance(tipo, DatetimeTZDtype) and tipo.unit == "ns"
    )

