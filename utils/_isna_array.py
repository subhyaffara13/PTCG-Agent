
def _isna_array(values: ArrayLike) -> npt.NDArray[np.bool_] | NDFrame:
    """
    Return an array indicating which values of the input array are NaN / NA.

    Parameters
    ----------
    obj: ndarray or ExtensionArray
        The input array whose elements are to be checked.

    Returns
    -------
    array-like
        Array of boolean values denoting the NA status of each element.
    """
    dtype = values.dtype
    result: npt.NDArray[np.bool_] | NDFrame

    if not isinstance(values, np.ndarray):
        # i.e. ExtensionArray
        # error: Incompatible types in assignment (expression has type
        # "Union[ndarray[Any, Any], ExtensionArraySupportsAnyAll]", variable has
        # type "ndarray[Any, dtype[bool_]]")
        result = values.isna()  # type: ignore[assignment]
    elif isinstance(values, np.rec.recarray):
        # GH 48526
        result = _isna_recarray_dtype(values)
    elif is_string_or_object_np_dtype(values.dtype):
        result = _isna_string_dtype(values)
    elif dtype.kind in "mM":
        # this is the NaT pattern
        result = values.view("i8") == iNaT
    else:
        result = np.isnan(values)

    return result

