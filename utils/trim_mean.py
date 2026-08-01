
def trim_mean(a, proportiontocut, axis=0):
    """Return mean of array after trimming a specified fraction of extreme values.

    Removes the specified proportion of elements from *each* end of the
    sorted array, then computes the mean of the remaining elements.

    Parameters
    ----------
    a : array_like
        Input array.
    proportiontocut : float
        Fraction of the most positive and most negative elements to remove.
        When the specified proportion does not result in an integer number of
        elements, the number of elements to trim is rounded down.
    axis : int or None, default: 0
        Axis along which the trimmed means are computed.
        If None, compute over the raveled array.

    Returns
    -------
    trim_mean : ndarray
        Mean of trimmed array.

    See Also
    --------
    trimboth : Remove a proportion of elements from each end of an array.
    tmean : Compute the mean after trimming values outside specified limits.

    Notes
    -----
    For 1-D array `a`, `trim_mean` is approximately equivalent to the following
    calculation::

        import numpy as np
        a = np.sort(a)
        m = int(proportiontocut * len(a))
        np.mean(a[m: len(a) - m])

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = [1, 2, 3, 5]
    >>> stats.trim_mean(x, 0.25)
    2.5

    When the specified proportion does not result in an integer number of
    elements, the number of elements to trim is rounded down.

    >>> stats.trim_mean(x, 0.24999) == np.mean(x)
    True

    Use `axis` to specify the axis along which the calculation is performed.

    >>> x2 = [[1, 2, 3, 5],
    ...       [10, 20, 30, 50]]
    >>> stats.trim_mean(x2, 0.25)
    array([ 5.5, 11. , 16.5, 27.5])
    >>> stats.trim_mean(x2, 0.25, axis=1)
    array([ 2.5, 25. ])

    """
    xp = array_namespace(a)

    a = xp.asarray(a)

    if xp_size(a) == 0:
        return _get_nan(a, xp=xp)

    if axis is None:
        a = xp_ravel(a)
        axis = 0

    nobs = _count_nonmasked(a, axis=axis, keepdims=True, xp=xp)
    lowercut = proportiontocut * nobs
    nobs, lowercut = ((nobs, int(lowercut)) if not is_marray(xp)
                      else (xp.astype(nobs, xp.int64), xp.astype(lowercut, xp.int64)))
    uppercut = nobs - lowercut
    if not is_marray(xp) and (lowercut > uppercut):
        raise ValueError("Proportion too big.")

    atmp = (np.partition(a, (lowercut, uppercut - 1), axis) if is_numpy(xp)
            else xp.sort(a, axis=axis))

    if is_marray(xp):
        indices = xp.arange(a.shape[-1])  # axis_nan_policy decorator -> axis=-1
        mask = (indices < lowercut) | (indices >= (nobs - lowercut)) | atmp.mask
        trimmed = xp.asarray(atmp.data, mask=mask.data)
    else:
        sl = [slice(None)] * atmp.ndim
        sl[axis] = slice(lowercut, uppercut)
        trimmed = atmp[tuple(sl)]

    trimmed = xp_promote(trimmed, force_floating=True, xp=xp)
    return xp.mean(trimmed, axis=axis)

