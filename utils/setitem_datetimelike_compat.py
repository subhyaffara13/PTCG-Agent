
def setitem_datetimelike_compat(values: np.ndarray, num_set: int, other):
    """
    Parameters
    ----------
    values : np.ndarray
    num_set : int
        For putmask, this is mask.sum()
    other : Any
    """
    if values.dtype == object:
        dtype, _ = infer_dtype_from(other)

        if lib.is_np_dtype(dtype, "mM"):
            # https://github.com/numpy/numpy/issues/12550
            #  timedelta64 will incorrectly cast to int
            if not is_list_like(other):
                other = [other] * num_set
            else:
                other = list(other)

    return other

