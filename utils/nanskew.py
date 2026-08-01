
def nanskew(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    mask: npt.NDArray[np.bool_] | None = None,
) -> float:
    """
    Compute the sample skewness.

    The statistic computed here is the adjusted Fisher-Pearson standardized
    moment coefficient G1. The algorithm computes this coefficient directly
    from the second and third central moment.

    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
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
    >>> s = pd.Series([1, np.nan, 1, 2])
    >>> nanops.nanskew(s.values)
    np.float64(1.7320508075688787)
    """
    mask = _maybe_get_mask(values, skipna, mask)
    if values.dtype.kind != "f":
        values = values.astype("f8")
        count = _get_counts(values.shape, mask, axis)
    else:
        count = _get_counts(values.shape, mask, axis, dtype=values.dtype)

    if skipna and mask is not None:
        values = values.copy()
        np.putmask(values, mask, 0)
    elif not skipna and mask is not None and mask.any():
        return np.nan

    with np.errstate(invalid="ignore", divide="ignore"):
        mean = values.sum(axis, dtype=np.float64) / count
    if axis is not None:
        mean = np.expand_dims(mean, axis)

    adjusted = values - mean
    if skipna and mask is not None:
        np.putmask(adjusted, mask, 0)
    adjusted2 = adjusted**2
    adjusted3 = adjusted2 * adjusted
    m2 = adjusted2.sum(axis, dtype=np.float64)
    m3 = adjusted3.sum(axis, dtype=np.float64)

    # floating point error. See comment in [nankurt]
    max_abs = np.abs(values).max(axis, initial=0.0)
    eps = np.finfo(m2.dtype).eps
    constant_tolerance2 = ((eps * max_abs) ** 2) * count
    constant_tolerance3 = ((eps * max_abs) ** 3) * count
    m2 = _zero_out_fperr(m2, constant_tolerance2)
    m3 = _zero_out_fperr(m3, constant_tolerance3)

    with np.errstate(invalid="ignore", divide="ignore"):
        result = (count * (count - 1) ** 0.5 / (count - 2)) * (m3 / m2**1.5)

    dtype = values.dtype
    if dtype.kind == "f":
        result = result.astype(dtype, copy=False)

    if isinstance(result, np.ndarray):
        result = np.where(m2 == 0, 0, result)
        result[count < 3] = np.nan
    else:
        result = dtype.type(0) if m2 == 0 else result
        if count < 3:
            return np.nan

    return result

