
def trimr(a, limits=None, inclusive=(True, True), axis=None):
    """
    Trims an array by masking some proportion of the data on each end.
    Returns a masked version of the input array.

    Parameters
    ----------
    a : sequence
        Input array.
    limits : {None, tuple}, optional
        Tuple of the percentages to cut on each side of the array, with respect
        to the number of unmasked data, as floats between 0. and 1.
        Noting n the number of unmasked data before trimming, the
        (n*limits[0])th smallest data and the (n*limits[1])th largest data are
        masked, and the total number of unmasked data after trimming is
        n*(1.-sum(limits)).  The value of one limit can be set to None to
        indicate an open interval.
    inclusive : {(True,True) tuple}, optional
        Tuple of flags indicating whether the number of data being masked on
        the left (right) end should be truncated (True) or rounded (False) to
        integers.
    axis : {None,int}, optional
        Axis along which to trim. If None, the whole array is trimmed, but its
        shape is maintained.

    """  # numpydoc ignore=RT01
    def _trimr1D(a, low_limit, up_limit, low_inclusive, up_inclusive):
        n = a.count()
        idx = a.argsort()
        if low_limit:
            if low_inclusive:
                lowidx = int(low_limit*n)
            else:
                lowidx = int(np.round(low_limit*n))
            a[idx[:lowidx]] = masked
        if up_limit is not None:
            if up_inclusive:
                upidx = n - int(n*up_limit)
            else:
                upidx = n - int(np.round(n*up_limit))
            a[idx[upidx:]] = masked
        return a

    a = ma.asarray(a)
    a.unshare_mask()
    if limits is None:
        return a

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

    if axis is None:
        shp = a.shape
        return _trimr1D(a.ravel(),lolim,uplim,loinc,upinc).reshape(shp)
    else:
        return ma.apply_along_axis(_trimr1D, axis, a, lolim,uplim,loinc,upinc)

