
def _maybe_null_out(
    result: np.ndarray | float | NaTType,
    axis: AxisInt | None,
    mask: npt.NDArray[np.bool_] | None,
    shape: tuple[int, ...],
    min_count: int = 1,
    datetimelike: bool = False,
) -> np.ndarray | float | NaTType:
    """
    Returns
    -------
    Dtype
        The product of all elements on a given axis. ( NaNs are treated as 1)
    """
    if mask is None and min_count == 0:
        # nothing to check; short-circuit
        return result

    if axis is not None and isinstance(result, np.ndarray):
        if mask is not None:
            null_mask = (mask.shape[axis] - mask.sum(axis) - min_count) < 0
        else:
            # we have no nulls, kept mask=None in _maybe_get_mask
            below_count = shape[axis] - min_count < 0
            new_shape = shape[:axis] + shape[axis + 1 :]
            null_mask = np.broadcast_to(below_count, new_shape)

        if np.any(null_mask):
            if datetimelike:
                # GH#60646 For datetimelike, no need to cast to float
                result[null_mask] = iNaT
            elif is_numeric_dtype(result):
                if np.iscomplexobj(result):
                    result = result.astype("c16")
                elif not is_float_dtype(result):
                    result = result.astype("f8", copy=False)
                result[null_mask] = np.nan
            else:
                # GH12941, use None to auto cast null
                result[null_mask] = None
    elif result is not NaT:
        if check_below_min_count(shape, mask, min_count):
            result_dtype = getattr(result, "dtype", None)
            if is_float_dtype(result_dtype):
                # error: Item "None" of "Optional[Any]" has no attribute "type"
                result = result_dtype.type("nan")  # type: ignore[union-attr]
            else:
                result = np.nan

    return result

