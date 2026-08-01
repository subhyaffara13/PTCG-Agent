
def tstd(a, limits=None, inclusive=(True, True), axis=0, ddof=1):
    """Compute the trimmed sample standard deviation.

    This function finds the sample standard deviation of given values,
    ignoring values outside the given `limits`.

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
    tstd : float
        Trimmed sample standard deviation.

    Notes
    -----
    `tstd` computes the unbiased sample standard deviation, i.e. it uses a
    correction factor ``n / (n - 1)``.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tstd(x)
    5.9160797830996161
    >>> stats.tstd(x, (3,17))
    4.4721359549995796

    """
    return tvar(a, limits, inclusive, axis, ddof, _no_deco=True)**0.5

