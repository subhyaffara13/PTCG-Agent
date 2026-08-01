
def is_numeric_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of a numeric dtype.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of a numeric dtype.

    See Also
    --------
    api.types.is_integer_dtype: Check whether the provided array or dtype
        is of an integer dtype.
    api.types.is_unsigned_integer_dtype: Check whether the provided array
        or dtype is of an unsigned integer dtype.
    api.types.is_signed_integer_dtype: Check whether the provided array
        or dtype is of a signed integer dtype.

    Examples
    --------
    >>> from pandas.api.types import is_numeric_dtype
    >>> is_numeric_dtype(str)
    False
    >>> is_numeric_dtype(int)
    True
    >>> is_numeric_dtype(float)
    True
    >>> is_numeric_dtype(np.uint64)
    True
    >>> is_numeric_dtype(np.datetime64)
    False
    >>> is_numeric_dtype(np.timedelta64)
    False
    >>> is_numeric_dtype(np.array(["a", "b"]))
    False
    >>> is_numeric_dtype(pd.Series([1, 2]))
    True
    >>> is_numeric_dtype(pd.Index([1, 2.0]))
    True
    >>> is_numeric_dtype(np.array([], dtype="m8[ns]"))
    False
    """
    return _is_dtype_type(
        arr_or_dtype, _classes_and_not_datetimelike(np.number, np.bool_)
    ) or _is_dtype(
        arr_or_dtype, lambda typ: isinstance(typ, ExtensionDtype) and typ._is_numeric
    )

