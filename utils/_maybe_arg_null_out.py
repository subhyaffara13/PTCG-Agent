
def _maybe_arg_null_out(
    result: np.ndarray,
    axis: AxisInt | None,
    mask: npt.NDArray[np.bool_] | None,
    skipna: bool,
) -> np.ndarray | int:
    # helper function for nanargmin/nanargmax
    if mask is None:
        return result

    if axis is None or not getattr(result, "ndim", False):
        if skipna and mask.all():
            raise ValueError("Encountered all NA values")
        elif not skipna and mask.any():
            raise ValueError("Encountered an NA value with skipna=False")
    elif skipna and mask.all(axis).any():
        raise ValueError("Encountered all NA values")
    elif not skipna and mask.any(axis).any():
        raise ValueError("Encountered an NA value with skipna=False")
    return result

