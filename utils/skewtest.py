
def skewtest(a, axis=0, alternative='two-sided'):
    """
    Tests whether the skew is different from the normal distribution.

    Parameters
    ----------
    a : array_like
        The data to be tested
    axis : int or None, optional
       Axis along which statistics are calculated. Default is 0.
       If None, compute over the whole array `a`.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the skewness of the distribution underlying the sample
          is different from that of the normal distribution (i.e. 0)
        * 'less': the skewness of the distribution underlying the sample
          is less than that of the normal distribution
        * 'greater': the skewness of the distribution underlying the sample
          is greater than that of the normal distribution

        .. versionadded:: 1.7.0

    Returns
    -------
    statistic : array_like
        The computed z-score for this test.
    pvalue : array_like
        A p-value for the hypothesis test

    Notes
    -----
    For more details about `skewtest`, see `scipy.stats.skewtest`.

    """
    a, axis = _chk_asarray(a, axis)
    if axis is None:
        a = a.ravel()
        axis = 0
    b2 = skew(a,axis)
    n = a.count(axis)
    if np.min(n) < 8:
        raise ValueError(f"skewtest is not valid with less than 8 samples; "
                         f"{np.min(n)} samples were given.")

    y = b2 * ma.sqrt(((n+1)*(n+3)) / (6.0*(n-2)))
    beta2 = (3.0*(n*n+27*n-70)*(n+1)*(n+3)) / ((n-2.0)*(n+5)*(n+7)*(n+9))
    W2 = -1 + ma.sqrt(2*(beta2-1))
    delta = 1/ma.sqrt(0.5*ma.log(W2))
    alpha = ma.sqrt(2.0/(W2-1))
    y = ma.where(y == 0, 1, y)
    Z = delta*ma.log(y/alpha + ma.sqrt((y/alpha)**2+1))
    pvalue = scipy.stats._stats_py._get_pvalue(Z, distributions.norm, alternative)

    return SkewtestResult(Z[()], pvalue[()])


def skewtest(a, axis=0, nan_policy='propagate', alternative='two-sided'):
    r"""Test whether the skew is different from the normal distribution.

    This function tests the null hypothesis that the skewness of
    the population that the sample was drawn from is the same
    as that of a corresponding normal distribution.

    Parameters
    ----------
    a : array
        The data to be tested. Must contain at least eight observations.
    axis : int or None, optional
       Axis along which statistics are calculated. Default is 0.
       If None, compute over the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the skewness of the distribution underlying the sample
          is different from that of the normal distribution (i.e. 0)
        * 'less': the skewness of the distribution underlying the sample
          is less than that of the normal distribution
        * 'greater': the skewness of the distribution underlying the sample
          is greater than that of the normal distribution

        .. versionadded:: 1.7.0

    Returns
    -------
    statistic : float
        The computed z-score for this test.
    pvalue : float
        The p-value for the hypothesis test.

    See Also
    --------
    :ref:`hypothesis_skewtest` : Extended example

    Notes
    -----
    The sample size must be at least 8.

    References
    ----------
    .. [1] R. B. D'Agostino, A. J. Belanger and R. B. D'Agostino Jr.,
            "A suggestion for using powerful and informative tests of
            normality", American Statistician 44, pp. 316-321, 1990.

    Examples
    --------

    >>> from scipy.stats import skewtest
    >>> skewtest([1, 2, 3, 4, 5, 6, 7, 8])
    SkewtestResult(statistic=1.0108048609177787, pvalue=0.3121098361421897)
    >>> skewtest([2, 8, 0, 4, 1, 9, 9, 0])
    SkewtestResult(statistic=0.44626385374196975, pvalue=0.6554066631275459)
    >>> skewtest([1, 2, 3, 4, 5, 6, 7, 8000])
    SkewtestResult(statistic=3.571773510360407, pvalue=0.0003545719905823133)
    >>> skewtest([100, 100, 100, 100, 100, 100, 100, 101])
    SkewtestResult(statistic=3.5717766638478072, pvalue=0.000354567720281634)
    >>> skewtest([1, 2, 3, 4, 5, 6, 7, 8], alternative='less')
    SkewtestResult(statistic=1.0108048609177787, pvalue=0.8439450819289052)
    >>> skewtest([1, 2, 3, 4, 5, 6, 7, 8], alternative='greater')
    SkewtestResult(statistic=1.0108048609177787, pvalue=0.15605491807109484)

    For a more detailed example, see :ref:`hypothesis_skewtest`.
    """
    xp = array_namespace(a)
    a, axis = _chk_asarray(a, axis, xp=xp)

    b2 = skew(a, axis, _no_deco=True)

    n = xp.asarray(_count_nonmasked(a, axis), dtype=b2.dtype, device=xp_device(a))
    n = xpx.at(n, n < 8).set(xp.nan)

    with np.errstate(divide='ignore', invalid='ignore'):
        y = b2 * xp.sqrt(((n + 1) * (n + 3)) / (6.0 * (n - 2)))
        beta2 = (3.0 * (n**2 + 27*n - 70) * (n+1) * (n+3) /
                 ((n-2.0) * (n+5) * (n+7) * (n+9)))
        W2 = -1 + xp.sqrt(2 * (beta2 - 1))
        delta = 1 / xp.sqrt(0.5 * xp.log(W2))
        alpha = xp.sqrt(2.0 / (W2 - 1))
        y = xp.where(y == 0, 1., y)
        Z = delta * xp.log(y / alpha + xp.sqrt((y / alpha)**2 + 1))
        pvalue = _get_pvalue(Z, _SimpleNormal(), alternative, xp=xp)

    Z = Z[()] if Z.ndim == 0 else Z
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue
    return SkewtestResult(Z, pvalue)

