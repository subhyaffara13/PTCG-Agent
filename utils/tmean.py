
def tmean(a, limits=None, inclusive=(True, True), axis=None):
    """
    Compute the trimmed mean.

    Parameters
    ----------
    a : array_like
        Array of values.
    limits : None or (lower limit, upper limit), optional
        Values in the input array less than the lower limit or greater than the
        upper limit will be ignored.  When limits is None (default), then all
        values are used.  Either of the limit values in the tuple can also be
        None representing a half-open interval.
    inclusive : (bool, bool), optional
        A tuple consisting of the (lower flag, upper flag).  These flags
        determine whether values exactly equal to the lower or upper limits
        are included.  The default value is (True, True).
    axis : int or None, optional
        Axis along which to operate. If None, compute over the
        whole array. Default is None.

    Returns
    -------
    tmean : float

    Notes
    -----
    For more details on `tmean`, see `scipy.stats.tmean`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import mstats
    >>> a = np.array([[6, 8, 3, 0],
    ...               [3, 9, 1, 2],
    ...               [8, 7, 8, 2],
    ...               [5, 6, 0, 2],
    ...               [4, 5, 5, 2]])
    ...
    ...
    >>> mstats.tmean(a, (2,5))
    3.3
    >>> mstats.tmean(a, (2,5), axis=0)
    masked_array(data=[4.0, 5.0, 4.0, 2.0],
                 mask=[False, False, False, False],
           fill_value=1e+20)

    """  # numpydoc ignore=RT03
    return trima(a, limits=limits, inclusive=inclusive).mean(axis=axis)


def tmean(a, limits=None, inclusive=(True, True), axis=None):
    """Compute the trimmed mean.

    This function finds the arithmetic mean of given values, ignoring values
    outside the given `limits`.

    Parameters
    ----------
    a : array_like
        Array of values.
    limits : None or (lower limit, upper limit), optional
        Values in the input array less than the lower limit or greater than the
        upper limit will be ignored.  When limits is None (default), then all
        values are used.  Either of the limit values in the tuple can also be
        None representing a half-open interval.
    inclusive : (bool, bool), optional
        A tuple consisting of the (lower flag, upper flag).  These flags
        determine whether values exactly equal to the lower or upper limits
        are included.  The default value is (True, True).
    axis : int or None, optional
        Axis along which to compute test. Default is None.

    Returns
    -------
    tmean : ndarray
        Trimmed mean.

    See Also
    --------
    trim_mean : Returns mean after trimming a proportion from both tails.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tmean(x)
    9.5
    >>> stats.tmean(x, (3,17))
    10.0

    """
    xp = array_namespace(a)
    a, mask = _put_val_to_limits(a, limits, inclusive, val=0., xp=xp)
    # explicit dtype specification required due to data-apis/array-api-compat#152
    sum = xp.sum(a, axis=axis, dtype=a.dtype)
    n = xp.sum(xp.asarray(~mask, dtype=a.dtype, device=xp_device(a)), axis=axis,
               dtype=a.dtype)
    mean = xpx.apply_where(n != 0, (sum, n), operator.truediv, fill_value=xp.nan)
    return mean[()] if mean.ndim == 0 else mean

