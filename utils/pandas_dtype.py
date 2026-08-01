
def pandas_dtype(dtype) -> DtypeObj:
    """
    Convert input into a pandas only dtype object or a numpy dtype object.

    Parameters
    ----------
    dtype : object
        The object to be converted into a dtype.

    Returns
    -------
    np.dtype or a pandas dtype
        The converted dtype, which can be either a numpy dtype or a pandas dtype.

    Raises
    ------
    TypeError if not a dtype

    See Also
    --------
    api.types.is_dtype : Return true if the condition is satisfied for the arr_or_dtype.

    Examples
    --------
    >>> pd.api.types.pandas_dtype(int)
    dtype('int64')
    """
    # short-circuit
    if isinstance(dtype, np.ndarray):
        return dtype.dtype
    elif isinstance(dtype, (np.dtype, ExtensionDtype)):
        return dtype

    # builtin aliases
    if dtype is str and using_string_dtype():
        from pandas.core.arrays.string_ import StringDtype

        return StringDtype(na_value=np.nan)

    # registered extension types
    result = registry.find(dtype)
    if result is not None:
        if isinstance(result, type):
            # GH 31356, GH 54592
            warnings.warn(
                f"Instantiating {result.__name__} without any arguments."
                f"Pass a {result.__name__} instance to silence this warning.",
                UserWarning,
                stacklevel=find_stack_level(),
            )
            result = result()
        return result

    # try a numpy dtype
    # raise a consistent TypeError if failed
    try:
        with warnings.catch_warnings():
            # TODO: warnings.catch_warnings can be removed when numpy>2.3.0
            # is the minimum version
            # GH#51523 - Series.astype(np.integer) doesn't show
            # numpy deprecation warning of np.integer
            # Hence enabling DeprecationWarning
            warnings.simplefilter("always", DeprecationWarning)
            npdtype = np.dtype(dtype)
    except TypeError:
        raise
    except ValueError as err:
        raise TypeError(f"data type '{dtype}' not understood") from err

    # Any invalid dtype (such as pd.Timestamp) should raise an error.
    # np.dtype(invalid_type).kind = 0 for such objects. However, this will
    # also catch some valid dtypes such as object, np.object_ and 'object'
    # which we safeguard against by catching them earlier and returning
    # np.dtype(valid_dtype) before this condition is evaluated.
    if is_hashable(dtype) and dtype in [
        object,
        np.object_,
        "object",
        "O",
        "object_",
    ]:
        # check hashability to avoid errors/DeprecationWarning when we get
        # here and `dtype` is an array
        return npdtype
    elif npdtype.kind == "O":
        raise TypeError(f"dtype '{dtype}' not understood")

    return npdtype

