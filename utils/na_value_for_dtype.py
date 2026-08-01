
def na_value_for_dtype(dtype: DtypeObj, compat: bool = True):
    """
    Return a dtype compat na value

    Parameters
    ----------
    dtype : string / dtype
    compat : bool, default True

    Returns
    -------
    np.dtype or a pandas dtype

    Examples
    --------
    >>> na_value_for_dtype(np.dtype("int64"))
    0
    >>> na_value_for_dtype(np.dtype("int64"), compat=False)
    nan
    >>> na_value_for_dtype(np.dtype("float64"))
    nan
    >>> na_value_for_dtype(np.dtype("complex128"))
    nan
    >>> na_value_for_dtype(np.dtype("bool"))
    False
    >>> na_value_for_dtype(np.dtype("datetime64[ns]"))
    np.datetime64('NaT','ns')
    """

    if isinstance(dtype, ExtensionDtype):
        return dtype.na_value
    elif dtype.kind in "mM":
        unit = np.datetime_data(dtype)[0]
        return dtype.type("NaT", unit)
    elif dtype.kind in "fc":
        return np.nan
    elif dtype.kind in "iu":
        if compat:
            return 0
        return np.nan
    elif dtype.kind == "b":
        if compat:
            return False
        return np.nan
    return np.nan

