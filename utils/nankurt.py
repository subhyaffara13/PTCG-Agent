
def nankurt(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    mask: npt.NDArray[np.bool_] | None = None,
) -> float:
    """
    Compute the sample excess kurtosis

    The statistic computed here is the adjusted Fisher-Pearson standardized
    moment coefficient G2, computed directly from the second and fourth
    central moment.

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
    >>> s = pd.Series([1, np.nan, 1, 3, 2])
    >>> nanops.nankurt(s.values)
    np.float64(-1.2892561983471076)
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
    adjusted4 = adjusted2**2
    m2 = adjusted2.sum(axis, dtype=np.float64)
    m4 = adjusted4.sum(axis, dtype=np.float64)

    # Several floating point errors may occur during the summation due to rounding.
    # This computation is similar to the one in Scipy
    # https://github.com/scipy/scipy/blob/04d6d9c460b1fed83f2919ecec3d743cfa2e8317/scipy/stats/_stats_py.py#L1429
    # With a few modifications, like using the maximum value instead of the averages
    # and some adaptations because they use the average and we use the sum for `m2`.
    # We need to estimate an upper bound to the error to consider the data constant.
    # Let's call:
    # x: true value in data
    # y: floating point representation
    # e: relative approximation error
    # n: number of observations in array
    #
    # We have that:
    # |x - y|/|x| <= e (See https://en.wikipedia.org/wiki/Machine_epsilon)
    # (|x - y|/|x|)² <= e²
    # Σ (|x - y|/|x|)² <= ne²
    #
    # Let's say that the fperr upper bound for m2 is constrained by the summation.
    # |m2 - y|/|m2| <= ne²
    # |m2 - y| <= n|m2|e²
    #
    # We will use max (x²) to estimate |m2|
    max_abs = np.abs(values).max(axis, initial=0.0)
    eps = np.finfo(m2.dtype).eps
    constant_tolerance2 = ((eps * max_abs) ** 2) * count
    constant_tolerance4 = ((eps * max_abs) ** 4) * count
    m2 = _zero_out_fperr(m2, constant_tolerance2)
    m4 = _zero_out_fperr(m4, constant_tolerance4)

    with np.errstate(invalid="ignore", divide="ignore"):
        adj = 3 * (count - 1) ** 2 / ((count - 2) * (count - 3))
        numerator = count * (count + 1) * (count - 1) * m4
        denominator = (count - 2) * (count - 3) * m2**2

    if not isinstance(denominator, np.ndarray):
        # if ``denom`` is a scalar, check these corner cases first before
        # doing division
        if count < 4:
            return np.nan
        if denominator == 0:
            return values.dtype.type(0)

    with np.errstate(invalid="ignore", divide="ignore"):
        result = numerator / denominator - adj

    dtype = values.dtype
    if dtype.kind == "f":
        result = result.astype(dtype, copy=False)

    if isinstance(result, np.ndarray):
        result = np.where(denominator == 0, 0, result)
        result[count < 4] = np.nan

    return result

