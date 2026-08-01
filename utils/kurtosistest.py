
def kurtosistest(a, axis=0, alternative='two-sided'):
    """
    Tests whether a dataset has normal kurtosis

    Parameters
    ----------
    a : array_like
        array of the sample data
    axis : int or None, optional
       Axis along which to compute test. Default is 0. If None,
       compute over the whole array `a`.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided': the kurtosis of the distribution underlying the sample
          is different from that of the normal distribution
        * 'less': the kurtosis of the distribution underlying the sample
          is less than that of the normal distribution
        * 'greater': the kurtosis of the distribution underlying the sample
          is greater than that of the normal distribution

        .. versionadded:: 1.7.0

    Returns
    -------
    statistic : array_like
        The computed z-score for this test.
    pvalue : array_like
        The p-value for the hypothesis test

    Notes
    -----
    For more details about `kurtosistest`, see `scipy.stats.kurtosistest`.

    """
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis=axis)
    if np.min(n) < 5:
        raise ValueError(f"kurtosistest requires at least 5 observations; "
                         f"{np.min(n)} observations were given.")
    if np.min(n) < 20:
        warnings.warn(f"kurtosistest only valid for n>=20 ... continuing "
                      f"anyway, n={np.min(n)}", stacklevel=2)

    b2 = kurtosis(a, axis, fisher=False)
    E = 3.0*(n-1) / (n+1)
    varb2 = 24.0*n*(n-2.)*(n-3) / ((n+1)*(n+1.)*(n+3)*(n+5))
    x = (b2-E)/ma.sqrt(varb2)
    sqrtbeta1 = 6.0*(n*n-5*n+2)/((n+7)*(n+9)) * np.sqrt((6.0*(n+3)*(n+5)) /
                                                        (n*(n-2)*(n-3)))
    A = 6.0 + 8.0/sqrtbeta1 * (2.0/sqrtbeta1 + np.sqrt(1+4.0/(sqrtbeta1**2)))
    term1 = 1 - 2./(9.0*A)
    denom = 1 + x*ma.sqrt(2/(A-4.0))
    if np.ma.isMaskedArray(denom):
        # For multi-dimensional array input
        denom[denom == 0.0] = masked
    elif denom == 0.0:
        denom = masked

    term2 = np.ma.where(denom > 0, ma.power((1-2.0/A)/denom, 1/3.0),
                        -ma.power(-(1-2.0/A)/denom, 1/3.0))
    Z = (term1 - term2) / np.sqrt(2/(9.0*A))
    pvalue = scipy.stats._stats_py._get_pvalue(Z, distributions.norm, alternative)

    return KurtosistestResult(Z[()], pvalue[()])


def kurtosistest(a, axis=0, nan_policy='propagate', alternative='two-sided'):
    r"""Test whether a dataset has normal kurtosis.

    This function tests the null hypothesis that the kurtosis
    of the population from which the sample was drawn is that
    of the normal distribution.

    Parameters
    ----------
    a : array
        Array of the sample data. Must contain at least five observations.
    axis : int or None, optional
       Axis along which to compute test. Default is 0. If None,
       compute over the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided': the kurtosis of the distribution underlying the sample
          is different from that of the normal distribution
        * 'less': the kurtosis of the distribution underlying the sample
          is less than that of the normal distribution
        * 'greater': the kurtosis of the distribution underlying the sample
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
    :ref:`hypothesis_kurtosistest` : Extended example

    Notes
    -----
    Valid only for n>20. This function uses the method described in [1]_.

    References
    ----------
    .. [1] F. J. Anscombe, W. J. Glynn, "Distribution of the kurtosis
       statistic b2 for normal samples", Biometrika, vol. 70, pp. 227-234, 1983.

    Examples
    --------

    >>> import numpy as np
    >>> from scipy.stats import kurtosistest
    >>> kurtosistest(list(range(20)))
    KurtosistestResult(statistic=-1.7058104152122062, pvalue=0.08804338332528348)
    >>> kurtosistest(list(range(20)), alternative='less')
    KurtosistestResult(statistic=-1.7058104152122062, pvalue=0.04402169166264174)
    >>> kurtosistest(list(range(20)), alternative='greater')
    KurtosistestResult(statistic=-1.7058104152122062, pvalue=0.9559783083373583)
    >>> rng = np.random.default_rng()
    >>> s = rng.normal(0, 1, 1000)
    >>> kurtosistest(s)
    KurtosistestResult(statistic=-1.475047944490622, pvalue=0.14019965402996987)

    For a more detailed example, see :ref:`hypothesis_kurtosistest`.
    """
    xp = array_namespace(a)
    a, axis = _chk_asarray(a, axis, xp=xp)

    b2 = kurtosis(a, axis, fisher=False, _no_deco=True)

    n = xp.asarray(_count_nonmasked(a, axis), dtype=b2.dtype, device=xp_device(a))
    n = xpx.at(n, n < 5).set(xp.nan)

    E = 3.0*(n-1) / (n+1)
    varb2 = 24.0*n*(n-2)*(n-3) / ((n+1)*(n+1.)*(n+3)*(n+5))  # [1]_ Eq. 1
    x = (b2-E) / varb2**0.5  # [1]_ Eq. 4
    # [1]_ Eq. 2:
    sqrtbeta1 = 6.0*(n*n-5*n+2)/((n+7)*(n+9)) * ((6.0*(n+3)*(n+5))
                                                 / (n*(n-2)*(n-3)))**0.5
    # [1]_ Eq. 3:
    A = 6.0 + 8.0/sqrtbeta1 * (2.0/sqrtbeta1 + (1+4.0/(sqrtbeta1**2))**0.5)
    term1 = 1 - 2/(9.0*A)
    denom = 1 + x * (2/(A-4.0))**0.5
    term2 = xp.sign(denom) * xp.where(denom == 0.0, xp.nan,
                                      ((1-2.0/A)/xp.abs(denom))**(1/3))
    if not is_lazy_array(denom) and xp.any(denom == 0):
        msg = ("Test statistic not defined in some cases due to division by "
               "zero. Return nan in that case...")
        warnings.warn(msg, RuntimeWarning, stacklevel=2)

    Z = (term1 - term2) / (2/(9.0*A))**0.5  # [1]_ Eq. 5
    pvalue = _get_pvalue(Z, _SimpleNormal(), alternative, xp=xp)

    Z = Z[()] if Z.ndim == 0 else Z
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue
    return KurtosistestResult(Z, pvalue)

