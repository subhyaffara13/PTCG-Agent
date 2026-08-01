
def is_dtype_equal(source, target) -> bool:
    """
    Check if two dtypes are equal.

    Parameters
    ----------
    source : type or str
        The first dtype to compare.
    target : type or str
        The second dtype to compare.

    Returns
    -------
    boolean
        Whether or not the two dtypes are equal.

    See Also
    --------
    api.types.is_categorical_dtype : Check whether the provided array or dtype
                                            is of the Categorical dtype.
    api.types.is_string_dtype : Check whether the provided array or dtype
                                       is of the string dtype.
    api.types.is_object_dtype : Check whether an array-like or dtype is of the
                                       object dtype.

    Examples
    --------
    >>> from pandas.api.types import is_dtype_equal
    >>> is_dtype_equal(int, float)
    False
    >>> is_dtype_equal("int", int)
    True
    >>> is_dtype_equal(object, "category")
    False
    >>> from pandas.api.types import CategoricalDtype
    >>> is_dtype_equal(CategoricalDtype(), "category")
    True
    >>> from pandas.api.types import DatetimeTZDtype
    >>> is_dtype_equal(DatetimeTZDtype(tz="UTC"), "datetime64")
    False
    """
    if isinstance(target, str):
        if not isinstance(source, str):
            # GH#38516 ensure we get the same behavior from
            #  is_dtype_equal(CDT, "category") and CDT == "category"
            try:
                src = _get_dtype(source)
                if isinstance(src, ExtensionDtype):
                    return src == target
            except (TypeError, AttributeError, ImportError):
                return False
    elif isinstance(source, str):
        return is_dtype_equal(target, source)

    try:
        source = _get_dtype(source)
        target = _get_dtype(target)
        return source == target
    except (TypeError, AttributeError, ImportError):
        # invalid comparison
        # object == category will hit this
        return False

