
def _ensure_dtype_type(value, dtype: np.dtype):
    """
    Ensure that the given value is an instance of the given dtype.

    e.g. if out dtype is np.complex64_, we should have an instance of that
    as opposed to a python complex object.

    Parameters
    ----------
    value : object
    dtype : np.dtype

    Returns
    -------
    object
    """
    # Start with exceptions in which we do _not_ cast to numpy types

    if dtype == _dtype_obj:
        return value

    # Note: before we get here we have already excluded isna(value)
    return dtype.type(value)

