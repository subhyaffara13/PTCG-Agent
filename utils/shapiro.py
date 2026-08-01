
def shapiro(x, *, axis=None):
    r"""Perform the Shapiro-Wilk test for normality.

    The Shapiro-Wilk test tests the null hypothesis that the
    data was drawn from a normal distribution.

    Parameters
    ----------
    x : array_like
        Array of sample data. Must contain at least three observations.
    axis : int or tuple of ints, default: 0
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    statistic : float
        The test statistic.
    p-value : float
        The p-value for the hypothesis test.

    See Also
    --------
    anderson : The Anderson-Darling test for normality
    kstest : The Kolmogorov-Smirnov test for goodness of fit.
    :ref:`hypothesis_shapiro` : Extended example

    Notes
    -----
    The algorithm used is described in [4]_, but censoring parameters as
    described are not implemented. For N > 5000 the W test statistic is
    accurate, but the p-value may not be.

    References
    ----------
    .. [1] https://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm
           :doi:`10.18434/M32189`
    .. [2] Shapiro, S. S. & Wilk, M.B, "An analysis of variance test for
           normality (complete samples)", Biometrika, 1965, Vol. 52,
           pp. 591-611, :doi:`10.2307/2333709`
    .. [3] Razali, N. M. & Wah, Y. B., "Power comparisons of Shapiro-Wilk,
           Kolmogorov-Smirnov, Lilliefors and Anderson-Darling tests", Journal
           of Statistical Modeling and Analytics, 2011, Vol. 2, pp. 21-33.
    .. [4] Royston, P. "A toolkit for testing for non-normality in complete and
           censored samples." Journal of the Royal Statistical Society: Series D
           (The Statistician) 42.1 (1993): 37-43.

    Examples
    --------

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> x = stats.norm.rvs(loc=5, scale=3, size=100, random_state=rng)
    >>> shapiro_test = stats.shapiro(x)
    >>> shapiro_test
    ShapiroResult(statistic=0.9813305735588074, pvalue=0.16855233907699585)
    >>> shapiro_test.statistic
    0.9813305735588074
    >>> shapiro_test.pvalue
    0.16855233907699585

    For a more detailed example, see :ref:`hypothesis_shapiro`.
    """
    # `x` is an array and axis=-1 due to _axis_nan_policy decorator
    xp = array_namespace(x)

    N = x.shape[-1]
    if N < 3:
        raise ValueError("Data must be at least length 3.")

    y = xp.sort(x, axis=-1)
    y -= x[..., N//2:N//2+1]  # subtract the median (or a nearby value); see gh-15777

    y = xp_promote(y, force_floating=True, xp=xp)
    w, pw = _swilk(y, xp=xp)
    if N > 5000:
        warnings.warn("scipy.stats.shapiro: For N > 5000, computed p-value "
                      f"may not be accurate. Current N is {N}.",
                      stacklevel=2)

    # `w` and `pw` are always Python floats, which are double precision.
    # We want to ensure that they are NumPy floats, so until dtypes are
    # respected, we can explicitly convert each to float64 (faster than
    # `np.array([w, pw])`).
    return ShapiroResult(w[()], pw[()])

