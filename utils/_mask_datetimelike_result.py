
def _mask_datetimelike_result(
    result: np.ndarray | np.datetime64 | np.timedelta64,
    axis: AxisInt | None,
    mask: npt.NDArray[np.bool_],
    orig_values: np.ndarray,
) -> np.ndarray | np.datetime64 | np.timedelta64 | NaTType:
    if isinstance(result, np.ndarray):
        # we need to apply the mask
        result = result.astype("i8").view(orig_values.dtype)
        axis_mask = mask.any(axis=axis)
        result[axis_mask] = iNaT
    elif mask.any():
        return np.int64(iNaT).view(orig_values.dtype)
    return result

