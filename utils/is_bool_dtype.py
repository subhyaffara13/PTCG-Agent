
def is_bool_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of a boolean dtype.

    This function verifies whether a given object is a boolean data type. The input
    can be an array or a dtype object. Accepted array types include instances
    of ``np.array``, ``pd.Series``, ``pd.Index``, and similar array-like structures.

    Parameters
    ----------
    arr_or_dtype : array-like or dtype
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of a boolean dtype.

    See Also
    --------
    api.types.is_bool : Check if an object is a boolean.

    Notes
    -----
    An ExtensionArray is considered boolean when the ``_is_boolean``
    attribute is set to True.

    Examples
    --------
    >>> from pandas.api.types import is_bool_dtype
    >>> is_bool_dtype(str)
    False
    >>> is_bool_dtype(int)
    False
    >>> is_bool_dtype(bool)
    True
    >>> is_bool_dtype(np.bool_)
    True
    >>> is_bool_dtype(np.array(["a", "b"]))
    False
    >>> is_bool_dtype(pd.Series([1, 2]))
    False
    >>> is_bool_dtype(np.array([True, False]))
    True
    >>> is_bool_dtype(pd.Categorical([True, False]))
    True
    >>> is_bool_dtype(pd.arrays.SparseArray([True, False]))
    True
    """
    if arr_or_dtype is None:
        return False
    try:
        dtype = _get_dtype(arr_or_dtype)
    except (TypeError, ValueError):
        return False

    if isinstance(dtype, CategoricalDtype):
        arr_or_dtype = dtype.categories
        # now we use the special definition for Index

    if isinstance(arr_or_dtype, ABCIndex):
        # Allow Index[object] that is all-bools or Index["boolean"]
        if arr_or_dtype.inferred_type == "boolean":
            if not is_bool_dtype(arr_or_dtype.dtype):
                # GH#52680
                warnings.warn(
                    "The behavior of is_bool_dtype with an object-dtype Index "
                    "of bool objects is deprecated. In a future version, "
                    "this will return False. Cast the Index to a bool dtype instead.",
                    Pandas4Warning,
                    stacklevel=2,
                )
            return True
        return False
    elif isinstance(dtype, ExtensionDtype):
        return getattr(dtype, "_is_boolean", False)

    return issubclass(dtype.type, np.bool_)

