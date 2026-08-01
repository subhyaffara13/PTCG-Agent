
def fligner(*samples, center='median', proportiontocut=0.05, axis=0):
    r"""Perform Fligner-Killeen test for equality of variance.

    Fligner's test tests the null hypothesis that all input samples
    are from populations with equal variances.  Fligner-Killeen's test is
    distribution free when populations are identical [2]_.

    Parameters
    ----------
    *samples : array_like
        Arrays of sample data.  Need not be the same length.
    center : {'mean', 'median', 'trimmed'}, optional
        Which statistics to use to center data points within each sample. Default
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
        The p-value for the hypothesis test.

    See Also
    --------
    bartlett : A parametric test for equality of k variances in normal samples
    levene : A robust parametric test for equality of k variances
    :ref:`hypothesis_fligner` : Extended example

    Notes
    -----
    As with Levene's test there are three variants of Fligner's test that
    differ by the measure of central tendency used in the test.  See `levene`
    for more information.

    Conover et al. (1981) examine many of the existing parametric and
    nonparametric tests by extensive simulations and they conclude that the
    tests proposed by Fligner and Killeen (1976) and Levene (1960) appear to be
    superior in terms of robustness of departures from normality and power
    [3]_.

    References
    ----------
    .. [1] Qu, A., Lindsay, B. G., and Li, B. (2000). Improving generalized
           estimating equations using quadratic inference functions.
           Biometrika, 87(4), 823-836.
           :doi:`10.1093/biomet/87.4.823`
    .. [2] Fligner, M.A. and Killeen, T.J. (1976). Distribution-free two-sample
           tests for scale. Journal of the American Statistical Association.
           71(353), 210-213.
    .. [3] Conover, W. J., Johnson, M. E. and Johnson M. M. (1981). A
           comparative study of tests for homogeneity of variances, with
           applications to the outer continental shelf bidding data.
           Technometrics, 23(4), 351-361.

    Examples
    --------

    >>> import numpy as np
    >>> from scipy import stats

    Test whether the lists `a`, `b` and `c` come from populations
    with equal variances.

    >>> a = [8.88, 9.12, 9.04, 8.98, 9.00, 9.08, 9.01, 8.85, 9.06, 8.99]
    >>> b = [8.88, 8.95, 9.29, 9.44, 9.15, 9.58, 8.36, 9.18, 8.67, 9.05]
    >>> c = [8.95, 9.12, 8.95, 8.85, 9.03, 8.84, 9.07, 8.98, 8.86, 8.98]
    >>> stat, p = stats.fligner(a, b, c)
    >>> p
    0.00450826080004775

    The small p-value suggests that the populations do not have equal
    variances.

    This is not surprising, given that the sample variance of `b` is much
    larger than that of `a` and `c`:

    >>> [np.var(x, ddof=1) for x in [a, b, c]]
    [0.007054444444444413, 0.13073888888888888, 0.008890000000000002]

    For a more detailed example, see :ref:`hypothesis_fligner`.
    """
    xp = array_namespace(*samples)

    if center not in ['mean', 'median', 'trimmed']:
        raise ValueError("center must be 'mean', 'median' or 'trimmed'.")

    k = len(samples)
    if k < 2:
        raise ValueError("Must provide at least two samples.")

    samples = xp_promote(*samples, force_floating=True, xp=xp)
    dtype = samples[0].dtype

    # Handle empty input
    for sample in samples:
        if sample.size == 0:
            NaN = _get_nan(*samples, xp=xp)
            return FlignerResult(NaN, NaN)

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
            # keepdims=True doesn't currently work for lazy arrays
            return _stats_py.trim_mean(x, proportiontocut, axis=-1)[..., xp.newaxis]

    lengths = [sample.shape[-1] for sample in samples]
    ni = [_count_nonmasked(sample, axis=-1, keepdims=True, xp=xp)
          for sample in samples]
    N = sum(ni)
    ni = [xp.squeeze(ni_, axis=-1) for ni_ in ni] if is_marray(xp) else ni

    # Implementation follows [3] pg 355 F-K.
    Xibar = [func(sample) for sample in samples]
    Xij_Xibar = [xp.abs(sample - Xibar_) for sample, Xibar_ in zip(samples, Xibar)]
    Xij_Xibar = xp.concat(Xij_Xibar, axis=-1)
    ranks = stats.rankdata(Xij_Xibar, method='average', axis=-1)
    a_Ni = special.ndtri(ranks / (2*(N + 1.0)) + 0.5)

    # [3] Equation 2.1
    splits = list(itertools.accumulate(lengths, initial=0))
    Ai = [a_Ni[..., i:j] for i, j in zip(splits[:-1], splits[1:])]
    Aibar = [xp.mean(Ai_, axis=-1) for Ai_ in Ai]
    abar = xp.mean(a_Ni, axis=-1)
    V2 = xp.var(a_Ni, axis=-1, correction=1)
    statistic = sum(ni_ * (Aibar_ - abar)**2 for ni_, Aibar_ in zip(ni, Aibar)) / V2

    chi2 = _SimpleChi2(xp.asarray(k-1, dtype=dtype))
    pval = _get_pvalue(statistic, chi2, alternative='greater', symmetric=False, xp=xp)
    return FlignerResult(statistic, pval)

