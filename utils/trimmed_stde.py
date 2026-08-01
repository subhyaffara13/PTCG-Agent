
def trimmed_stde(a, limits=(0.1,0.1), inclusive=(1,1), axis=None):
    """
    Returns the standard error of the trimmed mean along the given axis.

    Parameters
    ----------
    a : sequence
        Input array
    limits : {(0.1,0.1), tuple of float}, optional
        tuple (lower percentage, upper percentage) to cut  on each side of the
        array, with respect to the number of unmasked data.

        If n is the number of unmasked data before trimming, the values
        smaller than ``n * limits[0]`` and the values larger than
        ``n * `limits[1]`` are masked, and the total number of unmasked
        data after trimming is ``n * (1.-sum(limits))``.  In each case,
        the value of one limit can be set to None to indicate an open interval.
        If `limits` is None, no trimming is performed.
    inclusive : {(bool, bool) tuple} optional
        Tuple indicating whether the number of data being masked on each side
        should be rounded (True) or truncated (False).
    axis : int, optional
        Axis along which to trim.

    Returns
    -------
    trimmed_stde : scalar or ndarray

    """  # numpydoc ignore=RT03
    def _trimmed_stde_1D(a, low_limit, up_limit, low_inclusive, up_inclusive):
        "Returns the standard error of the trimmed mean for a 1D input data."
        n = a.count()
        idx = a.argsort()
        if low_limit:
            if low_inclusive:
                lowidx = int(low_limit*n)
            else:
                lowidx = np.round(low_limit*n)
            a[idx[:lowidx]] = masked
        if up_limit is not None:
            if up_inclusive:
                upidx = n - int(n*up_limit)
            else:
                upidx = n - np.round(n*up_limit)
            a[idx[upidx:]] = masked
        a[idx[:lowidx]] = a[idx[lowidx]]
        a[idx[upidx:]] = a[idx[upidx-1]]
        winstd = a.std(ddof=1)
        return winstd / ((1-low_limit-up_limit)*np.sqrt(len(a)))

    a = ma.array(a, copy=True, subok=True)
    a.unshare_mask()
    if limits is None:
        return a.std(axis=axis,ddof=1)/ma.sqrt(a.count(axis))
    if (not isinstance(limits,tuple)) and isinstance(limits,float):
        limits = (limits, limits)

    # Check the limits
    (lolim, uplim) = limits
    errmsg = "The proportion to cut from the %s should be between 0. and 1."
    if lolim is not None:
        if lolim > 1. or lolim < 0:
            raise ValueError(errmsg % 'beginning' + f"(got {lolim})")
    if uplim is not None:
        if uplim > 1. or uplim < 0:
            raise ValueError(errmsg % 'end' + f"(got {uplim})")

    (loinc, upinc) = inclusive
    if (axis is None):
        return _trimmed_stde_1D(a.ravel(),lolim,uplim,loinc,upinc)
    else:
        if a.ndim > 2:
            raise ValueError(f"Array 'a' must be at most two dimensional, "
                             f"but got a.ndim = {a.ndim}")
        return ma.apply_along_axis(_trimmed_stde_1D, axis, a,
                                   lolim,uplim,loinc,upinc)

