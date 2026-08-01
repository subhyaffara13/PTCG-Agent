
def _get_counts_nanvar(
    values_shape: Shape,
    mask: npt.NDArray[np.bool_] | None,
    axis: AxisInt | None,
    ddof: int,
    dtype: np.dtype = np.dtype(np.float64),
) -> tuple[float | np.ndarray, float | np.ndarray]:
    """
    Get the count of non-null values along an axis, accounting
    for degrees of freedom.

    Parameters
    ----------
    values_shape : Tuple[int, ...]
        shape tuple from values ndarray, used if mask is None
    mask : Optional[ndarray[bool]]
        locations in values that should be considered missing
    axis : Optional[int]
        axis to count along
    ddof : int
        degrees of freedom
    dtype : type, optional
        type to use for count

    Returns
    -------
    count : int, np.nan or np.ndarray
    d : int, np.nan or np.ndarray
    """
    count = _get_counts(values_shape, mask, axis, dtype=dtype)
    d = count - dtype.type(ddof)

    # always return NaN, never inf
    if is_float(count):
        if count <= ddof:
            # error: Incompatible types in assignment (expression has type
            # "float", variable has type "Union[floating[Any], ndarray[Any,
            # dtype[floating[Any]]]]")
            count = np.nan  # type: ignore[assignment]
            d = np.nan
    else:
        # count is not narrowed by is_float check
        count = cast(np.ndarray, count)
        mask = count <= ddof
        if mask.any():
            np.putmask(d, mask, np.nan)
            np.putmask(count, mask, np.nan)
    return count, d

