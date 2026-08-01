
def dtype_to_unit(dtype: DatetimeTZDtype | np.dtype | ArrowDtype) -> str:
    """
    Return the unit str corresponding to the dtype's resolution.

    Parameters
    ----------
    dtype : DatetimeTZDtype or np.dtype
        If np.dtype, we assume it is a datetime64 dtype.

    Returns
    -------
    str
    """
    if isinstance(dtype, DatetimeTZDtype):
        return dtype.unit
    elif isinstance(dtype, ArrowDtype):
        if dtype.kind not in "mM":
            raise ValueError(f"{dtype=} does not have a resolution.")
        return dtype.pyarrow_dtype.unit
    return np.datetime_data(dtype)[0]

