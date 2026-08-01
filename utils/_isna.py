
def _isna(obj):
    """
    Detect missing values, treating None, NaN or NA as null.

    Parameters
    ----------
    obj: ndarray or object value
        Input array or scalar value.

    Returns
    -------
    boolean ndarray or boolean
    """
    if is_scalar(obj):
        return libmissing.checknull(obj)
    elif isinstance(obj, ABCMultiIndex):
        raise NotImplementedError("isna is not defined for MultiIndex")
    elif isinstance(obj, type):
        return False
    elif isinstance(obj, (np.ndarray, ABCExtensionArray)):
        return _isna_array(obj)
    elif isinstance(obj, ABCIndex):
        # Try to use cached isna, which also short-circuits for integer dtypes
        #  and avoids materializing RangeIndex._values
        if not obj._can_hold_na:
            return obj.isna()
        return _isna_array(obj._values)

    elif isinstance(obj, ABCSeries):
        result = _isna_array(obj._values)
        # box
        result = obj._constructor(result, index=obj.index, name=obj.name, copy=False)
        return result
    elif isinstance(obj, ABCDataFrame):
        return obj.isna()
    elif isinstance(obj, list):
        return _isna_array(np.asarray(obj, dtype=object))
    elif hasattr(obj, "__array__"):
        return _isna_array(np.asarray(obj))
    else:
        return False

