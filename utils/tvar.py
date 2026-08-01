
def tvar(a, limits=None, inclusive=(True, True), axis=0, ddof=1):
    """
    Compute the trimmed variance

    This function computes the sample variance of an array of values,
    while ignoring values which are outside of given `limits`.

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
        Axis along which to operate. If None, compute over the
        whole array. Default is zero.
    ddof : int, optional
        Delta degrees of freedom. Default is 1.

    Returns
    -------
    tvar : float
        Trimmed variance.

    Notes
    -----
    For more details on `tvar`, see `scipy.stats.tvar`.

    """
    a = a.astype(float).ravel()
    if limits is None:
        n = (~a.mask).sum()  # todo: better way to do that?
        return np.ma.var(a) * n/(n-1.)
    am = _mask_to_limits(a, limits=limits, inclusive=inclusive)

    return np.ma.var(am, axis=axis, ddof=ddof)


def tvar(a, limits=None, inclusive=(True, True), axis=0, ddof=1):
    """Compute the trimmed variance.

    This function computes the sample variance of an array of values,
    while ignoring values which are outside of given `limits`.

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
    tvar : float
        Trimmed variance.

    Notes
    -----
    `tvar` computes the unbiased sample variance, i.e. it uses a correction
    factor ``n / (n - 1)``.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tvar(x)
    35.0
    >>> stats.tvar(x, (3,17))
    20.0

    """
    xp = array_namespace(a)
    a, _ = _put_val_to_limits(a, limits, inclusive, xp=xp)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SmallSampleWarning)
        # Currently, this behaves like nan_policy='omit' for alternative array
        # backends, but nan_policy='propagate' will be handled for other backends
        # by the axis_nan_policy decorator shortly.
        return _xp_var(a, correction=ddof, axis=axis, nan_policy='omit', xp=xp)

