
def hdquantiles_sd(data, prob=(.25, .5, .75), axis=None):
    """
    The standard error of the Harrell-Davis quantile estimates by jackknife.

    Parameters
    ----------
    data : array_like
        Data array.
    prob : sequence, optional
        Sequence of quantiles to compute.
    axis : int, optional
        Axis along which to compute the quantiles. If None, use a flattened
        array.

    Returns
    -------
    hdquantiles_sd : MaskedArray
        Standard error of the Harrell-Davis quantile estimates.

    See Also
    --------
    hdquantiles

    """
    def _hdsd_1D(data, prob):
        "Computes the std error for 1D arrays."
        xsorted = np.sort(data.compressed())
        n = len(xsorted)

        hdsd = np.empty(len(prob), float64)
        if n < 2:
            hdsd.flat = np.nan

        vv = np.arange(n) / float(n-1)
        betacdf = beta.cdf

        for (i,p) in enumerate(prob):
            _w = betacdf(vv, n*p, n*(1-p))
            w = _w[1:] - _w[:-1]
            # cumulative sum of weights and data points if
            # ith point is left out for jackknife
            mx_ = np.zeros_like(xsorted)
            mx_[1:] = np.cumsum(w * xsorted[:-1])
            # similar but from the right
            mx_[:-1] += np.cumsum(w[::-1] * xsorted[:0:-1])[::-1]
            hdsd[i] = np.sqrt(mx_.var() * (n - 1))
        return hdsd

    # Initialization & checks
    data = ma.array(data, copy=False, dtype=float64)
    p = np.atleast_1d(np.asarray(prob))
    # Computes quantiles along axis (or globally)
    if (axis is None):
        result = _hdsd_1D(data, p)
    else:
        if data.ndim > 2:
            raise ValueError(f"Array 'data' must be at most two dimensional, "
                             f"but got data.ndim = {data.ndim}")
        result = ma.apply_along_axis(_hdsd_1D, axis, data, p)

    return ma.fix_invalid(result, copy=False).ravel()

