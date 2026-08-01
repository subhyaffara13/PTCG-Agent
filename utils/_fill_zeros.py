
def _fill_zeros(result: np.ndarray, x, y) -> np.ndarray:
    """
    If this is a reversed op, then flip x,y

    If we have an integer value (or array in y)
    and we have 0's, fill them with np.nan,
    return the result.

    Mask the nan's from x.
    """
    if result.dtype.kind == "f":
        return result

    is_variable_type = hasattr(y, "dtype")
    is_scalar_type = not isinstance(y, np.ndarray)

    if not is_variable_type and not is_scalar_type:
        # e.g. test_series_ops_name_retention with mod we get here with list/tuple
        return result

    if is_scalar_type:
        y = np.array(y)

    if y.dtype.kind in "iu":
        ymask = y == 0
        if ymask.any():
            # GH#7325, mask and nans must be broadcastable
            mask = ymask & ~np.isnan(result)

            # GH#9308 doing ravel on result and mask can improve putmask perf,
            #  but can also make unwanted copies.
            result = result.astype("float64", copy=False)

            np.putmask(result, mask, np.nan)

    return result

