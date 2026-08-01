
def is_object_or_nan_string_dtype(dtype):
    """
    Check if string-like dtype is following NaN semantics, i.e. is object
    dtype or a NaN-variant of the StringDtype.
    """
    return (isinstance(dtype, np.dtype) and dtype == "object") or (
        dtype.na_value is np.nan
    )

