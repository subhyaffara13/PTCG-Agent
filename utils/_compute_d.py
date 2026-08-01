
def _compute_d(cdfvals, x, sign, xp=None):
    """Computes D+/D- as used in the Kolmogorov-Smirnov test.

    Vectorized along the last axis.

    Parameters
    ----------
    cdfvals : array_like
        Sorted array of CDF values between 0 and 1
    x: array_like
        Sorted array of the stochastic variable itself
    sign: int
        Indicates whether to compute D+ (+1) or D- (-1).

    Returns
    -------
    D : float or array
        The maximum distance of the CDF values below/above (D+/D-) Uniform(0, 1).
    loc_max : float or array
        The location at which the maximum is reached.
    """
    xp = array_namespace(cdfvals, x) if xp is None else xp
    length = cdfvals.shape[-1]
    n = _count_nonmasked(cdfvals, axis=-1, keepdims=True)
    D = (xp.arange(1.0, length + 1, dtype=x.dtype) / n - cdfvals if sign == +1
         else (cdfvals - xp.arange(0.0, length, dtype=x.dtype) / n))
    amax = xp.argmax(D, axis=-1, keepdims=True)
    loc_max = xp.squeeze(xp.take_along_axis(x, amax, axis=-1), axis=-1)
    D = xp.squeeze(xp.take_along_axis(D, amax, axis=-1), axis=-1)
    return D[()] if D.ndim == 0 else D, loc_max[()] if loc_max.ndim == 0 else loc_max

