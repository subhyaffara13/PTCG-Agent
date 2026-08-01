
def _is_dtype(arr_or_dtype, condition) -> bool:
    """
    Return true if the condition is satisfied for the arr_or_dtype.

    Parameters
    ----------
    arr_or_dtype : array-like, str, np.dtype, or ExtensionArrayType
        The array-like or dtype object whose dtype we want to extract.
    condition : callable[Union[np.dtype, ExtensionDtype]]

    Returns
    -------
    bool

    """
    if arr_or_dtype is None:
        return False
    try:
        dtype = _get_dtype(arr_or_dtype)
    except (TypeError, ValueError):
        return False
    return condition(dtype)

