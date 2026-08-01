
def nansem(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    ddof: int = 1,
    mask: npt.NDArray[np.bool_] | None = None,
) -> float:
    """
    Compute the standard error in the mean along given axis while ignoring NaNs

    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
    ddof : int, default 1
        Delta Degrees of Freedom. The divisor used in calculations is N - ddof,
        where N represents the number of elements.
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    result : float64
        Unless input is a float array, in which case use the same
        precision as the input array.

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, np.nan, 2, 3])
    >>> nanops.nansem(s.values)
     np.float64(0.5773502691896258)
    """
    # This checks if non-numeric-like data is passed with numeric_only=False
    # and raises a TypeError otherwise
    nanvar(values, axis=axis, skipna=skipna, ddof=ddof, mask=mask)

    mask = _maybe_get_mask(values, skipna, mask)
    # Convert to bottleneck return a float
    if values.dtype.kind not in "fc":
        values = values.astype("f8")

    if not skipna and mask is not None and mask.any():
        return np.nan

    dtype_count = np.dtype(np.float64)
    if values.dtype.kind == "f":
        dtype_count = values.dtype
    count, _ = _get_counts_nanvar(values.shape, mask, axis, ddof, dtype_count)
    var = nanvar(values, axis=axis, skipna=skipna, ddof=ddof, mask=mask)

    return np.sqrt(var) / np.sqrt(count)

