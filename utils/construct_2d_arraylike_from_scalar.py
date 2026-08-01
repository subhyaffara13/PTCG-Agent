
def construct_2d_arraylike_from_scalar(
    value: Scalar, length: int, width: int, dtype: np.dtype, copy: bool
) -> np.ndarray:
    shape = (length, width)

    if dtype.kind in "mM":
        value = _maybe_box_and_unbox_datetimelike(value, dtype)
    elif dtype == _dtype_obj:
        if isinstance(value, (np.timedelta64, np.datetime64)):
            # calling np.array below would cast to pytimedelta/pydatetime
            out = np.empty(shape, dtype=object)
            out.fill(value)
            return out

    # Attempt to coerce to a numpy array
    try:
        if not copy:
            arr = np.asarray(value, dtype=dtype)
        else:
            arr = np.array(value, dtype=dtype, copy=copy)
    except (ValueError, TypeError) as err:
        raise TypeError(
            f"DataFrame constructor called with incompatible data and dtype: {err}"
        ) from err

    if arr.ndim != 0:
        raise ValueError("DataFrame constructor not properly called!")

    return np.full(shape, arr)

