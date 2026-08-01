
def tsem(a, limits=None, inclusive=(True, True), axis=0, ddof=1):
    """
    Compute the trimmed standard error of the mean.

    This function finds the standard error of the mean for given
    values, ignoring values outside the given `limits`.

    Parameters
    ----------
    a : array_like
        array of values
    limits : None or (lower limit, upper limit), optional
        Values in the input array less than the lower limit or greater than the
        upper limit will be ignored. When limits is None, then all values are
        used. Either of the limit values in the tuple can also be None
        representing a half-open interval.  The default value is None.
    inclusive : (bool, bool), optional
        A tuple consisting of the (lower flag, upper flag).  These flags
        determine whether values exactly equal to the lower or upper limits
        are included.  The default value is (True, True).
    axis : int or None, optional
        Axis along which to operate. If None, compute over the
        whole array. Default is zero.
    ddof : int, optional
        Delta degrees of freedom. Default is 1.

    Returns
    -------
    tsem : float

    Notes
    -----
    For more details on `tsem`, see `scipy.stats.tsem`.

    """  # numpydoc ignore=RT03
    a = ma.asarray(a).ravel()
    if limits is None:
        n = float(a.count())
        return a.std(axis=axis, ddof=ddof)/ma.sqrt(n)

    am = trima(a.ravel(), limits, inclusive)
    sd = np.sqrt(am.var(axis=axis, ddof=ddof))
    return sd / np.sqrt(am.count())


def tsem(a, limits=None, inclusive=(True, True), axis=0, ddof=1):
    """Compute the trimmed standard error of the mean.

    This function finds the standard error of the mean for given
    values, ignoring values outside the given `limits`.

    Parameters
    ----------
    a : array_like
        Array of values.
    limits : None or (lower limit, upper limit), optional
        Values in the input array less than the lower limit or greater than the
        upper limit will be ignored. When limits is None, then all values are
        used. Either of the limit values in the tuple can also be None
        representing a half-open interval.  The default value is None.
    inclusive : (bool, bool), optional
        A tuple consisting of the (lower flag, upper flag).  These flags
        determine whether values exactly equal to the lower or upper limits
        are included.  The default value is (True, True).
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over the
        whole array `a`.
    ddof : int, optional
        Delta degrees of freedom.  Default is 1.

    Returns
    -------
    tsem : float
        Trimmed standard error of the mean.

    Notes
    -----
    `tsem` uses unbiased sample standard deviation, i.e. it uses a
    correction factor ``n / (n - 1)``.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tsem(x)
    1.3228756555322954
    >>> stats.tsem(x, (3,17))
    1.1547005383792515

    """
    xp = array_namespace(a)
    a, _ = _put_val_to_limits(a, limits, inclusive, xp=xp)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SmallSampleWarning)
        # Currently, this behaves like nan_policy='omit' for alternative array
        # backends, but nan_policy='propagate' will be handled for other backends
        # by the axis_nan_policy decorator shortly.
        sd = _xp_var(a, correction=ddof, axis=axis, nan_policy='omit', xp=xp)**0.5

    not_nan = xp.astype(~xp.isnan(a), a.dtype)
    n_obs = xp.sum(not_nan, axis=axis, dtype=sd.dtype)
    return sd / n_obs**0.5

