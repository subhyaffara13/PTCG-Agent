
def is_period_dtype(arr_or_dtype) -> bool:
    """
    Check whether an array-like or dtype is of the Period dtype.

    .. deprecated:: 2.2.0
        Use isinstance(dtype, pd.PeriodDtype) instead.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array-like or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array-like or dtype is of the Period dtype.

    See Also
    --------
    api.types.is_timedelta64_ns_dtype : Check whether the provided array or dtype is
        of the timedelta64[ns] dtype.
    api.types.is_timedelta64_dtype: Check whether an array-like or dtype
        is of the timedelta64 dtype.

    Examples
    --------
    >>> from pandas.api.types import is_period_dtype
    >>> is_period_dtype(object)
    False
    >>> is_period_dtype(pd.PeriodDtype(freq="D"))
    True
    >>> is_period_dtype([1, 2, 3])
    False
    >>> is_period_dtype(pd.Period("2017-01-01"))
    False
    >>> is_period_dtype(pd.PeriodIndex([], freq="Y"))
    True
    """
    warnings.warn(
        "is_period_dtype is deprecated and will be removed in a future version. "
        "Use `isinstance(dtype, pd.PeriodDtype)` instead",
        Pandas4Warning,
        stacklevel=2,
    )
    if isinstance(arr_or_dtype, ExtensionDtype):
        # GH#33400 fastpath for dtype object
        return arr_or_dtype.type is Period

    if arr_or_dtype is None:
        return False
    return PeriodDtype.is_dtype(arr_or_dtype)

