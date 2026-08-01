
def levene(*samples, center='median', proportiontocut=0.05, axis=0):
    r"""Perform Levene test for equal variances.

    The Levene test tests the null hypothesis that all input samples
    are from populations with equal variances.  Levene's test is an
    alternative to Bartlett's test `bartlett` in the case where
    there are significant deviations from normality.

    Parameters
    ----------
    *samples : array_like
        The sample data, possibly with different lengths.
    center : {'mean', 'median', 'trimmed'}, optional
        Which statistics to use to center data points within each sample.  Default
        is 'median'.
    proportiontocut : float, optional
        When `center` is 'trimmed', this gives the proportion of data points
        to cut from each end. (See `scipy.stats.trim_mean`.)
        Default is 0.05.
    axis : int or tuple of ints, default: 0
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    statistic : float
        The test statistic.
    pvalue : float
        The p-value for the test.

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    bartlett : A parametric test for equality of k variances in normal samples
    :ref:`hypothesis_levene` : Extended example

    Notes
    -----
    Three variations of Levene's test are possible.  The possibilities
    and their recommended usages are:

    * 'median' : Recommended for skewed (non-normal) distributions>
    * 'mean' : Recommended for symmetric, moderate-tailed distributions.
    * 'trimmed' : Recommended for heavy-tailed distributions.

    The test version using the mean was proposed in the original article
    of Levene ([2]_) while the median and trimmed mean have been studied by
    Brown and Forsythe ([3]_), sometimes also referred to as Brown-Forsythe
    test.

    References
    ----------
    .. [1] https://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm
    .. [2] Levene, H. (1960). In Contributions to Probability and Statistics:
           Essays in Honor of Harold Hotelling, I. Olkin et al. eds.,
           Stanford University Press, pp. 278-292.
    .. [3] Brown, M. B. and Forsythe, A. B. (1974), Journal of the American
           Statistical Association, 69, 364-367

    Examples
    --------

    Test whether the lists `a`, `b` and `c` come from populations
    with equal variances.

    >>> import numpy as np
    >>> from scipy import stats
    >>> a = [8.88, 9.12, 9.04, 8.98, 9.00, 9.08, 9.01, 8.85, 9.06, 8.99]
    >>> b = [8.88, 8.95, 9.29, 9.44, 9.15, 9.58, 8.36, 9.18, 8.67, 9.05]
    >>> c = [8.95, 9.12, 8.95, 8.85, 9.03, 8.84, 9.07, 8.98, 8.86, 8.98]
    >>> stat, p = stats.levene(a, b, c)
    >>> p
    0.002431505967249681

    The small p-value suggests that the populations do not have equal
    variances.

    This is not surprising, given that the sample variance of `b` is much
    larger than that of `a` and `c`:

    >>> [np.var(x, ddof=1) for x in [a, b, c]]
    [0.007054444444444413, 0.13073888888888888, 0.008890000000000002]

    For a more detailed example, see :ref:`hypothesis_levene`.
    """
    xp = array_namespace(*samples)

    if center not in ['mean', 'median', 'trimmed']:
        raise ValueError("center must be 'mean', 'median' or 'trimmed'.")

    k = len(samples)
    if k < 2:
        raise ValueError("Must provide at least two samples.")

    if center == 'median':

        def func(x):
            return (xp.median(x, axis=-1, keepdims=True)
                    if (is_numpy(xp) or is_dask(xp))
                    else stats.quantile(x, 0.5, axis=-1, keepdims=True))

    elif center == 'mean':

        def func(x):
            return xp.mean(x, axis=-1, keepdims=True)

    else:  # center == 'trimmed'

        def func(x):
            # keepdims=True doesn't currently work for Dask
            return _stats_py.trim_mean(x, proportiontocut, axis=-1)[..., xp.newaxis]

    Nis = [_count_nonmasked(sample, axis=-1, keepdims=True, xp=xp)
           for sample in samples]
    Ycis = [func(sample) for sample in samples]
    Ntot = sum(Nis)

    # compute Zij's
    Zijs = [xp.abs(sample - Yc) for sample, Yc in zip(samples, Ycis)]

    # compute Zbari
    Zbaris = [xp.mean(Zij, axis=-1, keepdims=True) for Zij in Zijs]
    Zbar = sum(Ni*Zbari for Ni, Zbari in zip(Nis, Zbaris)) / Ntot

    # compute numerator and denominator
    dfd = (Ntot - k)
    numer = dfd * sum(Ni * (Zbari - Zbar)**2
                      for Ni, Zbari in zip(Nis, Zbaris))
    dfn = (k - 1.0)
    denom = dfn * sum(xp.sum((Zij - Zbari)**2, axis=-1, keepdims=True)
                      for Zij, Zbari in zip(Zijs, Zbaris))

    W = numer / denom
    W = xp.squeeze(W, axis=-1)
    dfd = xp.squeeze(dfd, axis=-1) if is_marray(xp) else dfd
    dfn, dfd = xp.asarray(dfn, dtype=W.dtype), xp.asarray(dfd, dtype=W.dtype)
    pval = _get_pvalue(W, _SimpleF(dfn, dfd), 'greater', xp=xp)
    W = W[()] if W.ndim == 0 else W
    pval = pval[()] if pval.ndim == 0 else pval
    return LeveneResult(W, pval)

