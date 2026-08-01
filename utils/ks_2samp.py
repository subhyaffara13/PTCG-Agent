
def ks_2samp(data1, data2, alternative="two-sided", method='auto'):
    """
    Computes the Kolmogorov-Smirnov test on two samples.

    Missing values in `x` and/or `y` are discarded.

    Parameters
    ----------
    data1 : array_like
        First data set
    data2 : array_like
        Second data set
    alternative : {'two-sided', 'less', 'greater'}, optional
        Indicates the alternative hypothesis.  Default is 'two-sided'.
    method : {'auto', 'exact', 'asymp'}, optional
        Defines the method used for calculating the p-value.
        The following options are available (default is 'auto'):

        * 'auto' : use 'exact' for small size arrays, 'asymp' for large
        * 'exact' : use approximation to exact distribution of test statistic
        * 'asymp' : use asymptotic distribution of test statistic

    Returns
    -------
    d : float
        Value of the Kolmogorov Smirnov test
    p : float
        Corresponding p-value.

    """
    # Ideally this would be accomplished by
    # ks_2samp = scipy.stats._stats_py.ks_2samp
    # but the circular dependencies between _mstats_basic and stats prevent that.
    alternative = {'t': 'two-sided', 'g': 'greater', 'l': 'less'}.get(
       alternative.lower()[0], alternative)
    return scipy.stats._stats_py.ks_2samp(data1, data2,
                                          alternative=alternative,
                                          method=method)


def ks_2samp(data1, data2, alternative='two-sided', method='auto', *, axis=0):
    """
    Performs the two-sample Kolmogorov-Smirnov test for goodness of fit.

    This test compares the underlying continuous distributions F(x) and G(x)
    of two independent samples.  See Notes for a description of the available
    null and alternative hypotheses.

    Parameters
    ----------
    data1, data2 : array_like, 1-Dimensional
        Two arrays of sample observations assumed to be drawn from a continuous
        distribution, sample sizes can be different.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the null and alternative hypotheses. Default is 'two-sided'.
        Please see explanations in the Notes below.
    method : {'auto', 'exact', 'asymp'}, optional
        Defines the method used for calculating the p-value.
        The following options are available (default is 'auto'):

        * 'auto' : use 'exact' for small size arrays, 'asymp' for large
        * 'exact' : use exact distribution of test statistic
        * 'asymp' : use asymptotic distribution of test statistic

    axis : int or tuple of ints, default: 0
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    res: KstestResult
        An object containing attributes:

        statistic : float
            KS test statistic.
        pvalue : float
            One-tailed or two-tailed p-value.
        statistic_location : float
            Value from `data1` or `data2` corresponding with the KS statistic;
            i.e., the distance between the empirical distribution functions is
            measured at this observation.
        statistic_sign : int
            +1 if the empirical distribution function of `data1` exceeds
            the empirical distribution function of `data2` at
            `statistic_location`, otherwise -1.

    See Also
    --------
    kstest, ks_1samp, epps_singleton_2samp, anderson_ksamp

    Notes
    -----
    There are three options for the null and corresponding alternative
    hypothesis that can be selected using the `alternative` parameter.

    - `less`: The null hypothesis is that F(x) >= G(x) for all x; the
      alternative is that F(x) < G(x) for at least one x. The statistic
      is the magnitude of the minimum (most negative) difference between the
      empirical distribution functions of the samples.

    - `greater`: The null hypothesis is that F(x) <= G(x) for all x; the
      alternative is that F(x) > G(x) for at least one x. The statistic
      is the maximum (most positive) difference between the empirical
      distribution functions of the samples.

    - `two-sided`: The null hypothesis is that the two distributions are
      identical, F(x)=G(x) for all x; the alternative is that they are not
      identical. The statistic is the maximum absolute difference between the
      empirical distribution functions of the samples.

    Note that the alternative hypotheses describe the *CDFs* of the
    underlying distributions, not the observed values of the data. For example,
    suppose x1 ~ F and x2 ~ G. If F(x) > G(x) for all x, the values in
    x1 tend to be less than those in x2.

    If the KS statistic is large, then the p-value will be small, and this may
    be taken as evidence against the null hypothesis in favor of the
    alternative.

    If ``method='exact'``, `ks_2samp` attempts to compute an exact p-value,
    that is, the probability under the null hypothesis of obtaining a test
    statistic value as extreme as the value computed from the data.
    If ``method='asymp'``, the asymptotic Kolmogorov-Smirnov distribution is
    used to compute an approximate p-value.
    If ``method='auto'``, an exact p-value computation is attempted if both
    sample sizes are less than 10000; otherwise, the asymptotic method is used.
    In any case, if an exact p-value calculation is attempted and fails, a
    warning will be emitted, and the asymptotic p-value will be returned.

    The 'two-sided' 'exact' computation computes the complementary probability
    and then subtracts from 1.  As such, the minimum probability it can return
    is about 1e-16.  While the algorithm itself is exact, numerical
    errors may accumulate for large sample sizes.   It is most suited to
    situations in which one of the sample sizes is only a few thousand.

    We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk [1]_.

    References
    ----------
    .. [1] Hodges, J.L. Jr.,  "The Significance Probability of the Smirnov
           Two-Sample Test," Arkiv fiur Matematik, 3, No. 43 (1958), 469-486.

    Examples
    --------
    Suppose we wish to test the null hypothesis that two samples were drawn
    from the same distribution.
    We choose a confidence level of 95%; that is, we will reject the null
    hypothesis in favor of the alternative if the p-value is less than 0.05.

    If the first sample were drawn from a uniform distribution and the second
    were drawn from the standard normal, we would expect the null hypothesis
    to be rejected.

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> sample1 = stats.uniform.rvs(size=100, random_state=rng)
    >>> sample2 = stats.norm.rvs(size=110, random_state=rng)
    >>> stats.ks_2samp(sample1, sample2)
    KstestResult(statistic=0.5454545454545454,
                 pvalue=7.37417839555191e-15,
                 statistic_location=-0.014071496412861274,
                 statistic_sign=-1)


    Indeed, the p-value is lower than our threshold of 0.05, so we reject the
    null hypothesis in favor of the default "two-sided" alternative: the data
    were *not* drawn from the same distribution.

    When both samples are drawn from the same distribution, we expect the data
    to be consistent with the null hypothesis most of the time.

    >>> sample1 = stats.norm.rvs(size=105, random_state=rng)
    >>> sample2 = stats.norm.rvs(size=95, random_state=rng)
    >>> stats.ks_2samp(sample1, sample2)
    KstestResult(statistic=0.10927318295739348,
                 pvalue=0.5438289009927495,
                 statistic_location=-0.1670157701848795,
                 statistic_sign=-1)

    As expected, the p-value of 0.54 is not below our threshold of 0.05, so
    we cannot reject the null hypothesis.

    Suppose, however, that the first sample were drawn from
    a normal distribution shifted toward greater values. In this case,
    the cumulative density function (CDF) of the underlying distribution tends
    to be *less* than the CDF underlying the second sample. Therefore, we would
    expect the null hypothesis to be rejected with ``alternative='less'``:

    >>> sample1 = stats.norm.rvs(size=105, loc=0.5, random_state=rng)
    >>> stats.ks_2samp(sample1, sample2, alternative='less')
    KstestResult(statistic=0.4055137844611529,
                 pvalue=3.5474563068855554e-08,
                 statistic_location=-0.13249370614972575,
                 statistic_sign=-1)

    and indeed, with p-value smaller than our threshold, we reject the null
    hypothesis in favor of the alternative.

    """
    # because of the _axis_nan_policy decorator, we can assume the arrays
    # are broadcasted and `axis=-1`
    mode = method

    if mode not in ['auto', 'exact', 'asymp']:
        raise ValueError(f'Invalid value for mode: {mode}')
    alternative = {'t': 'two-sided', 'g': 'greater', 'l': 'less'}.get(
        alternative.lower()[0], alternative)
    if alternative not in ['two-sided', 'less', 'greater']:
        raise ValueError(f'Invalid value for alternative: {alternative}')
    MAX_AUTO_N = 10000  # 'auto' will attempt to be exact if n1,n2 <= MAX_AUTO_N

    xp = array_namespace(data1, data2)
    data1 = xp.sort(data1, axis=-1)
    data2 = xp.sort(data2, axis=-1)
    n1 = data1.shape[-1]
    n2 = data2.shape[-1]
    if min(n1, n2) == 0:
        raise ValueError('Data passed to ks_2samp must not be empty')

    data_all = xp.concat((data1, data2), axis=-1)
    batch_shape = data_all.shape[:-1]
    dtype = xp_result_type(data1, data2, force_floating=True, xp=xp)

    if is_marray(xp):
        # Previously, we used this algorithm for all backends:
        n1 = xp.astype(_count_nonmasked(data1, axis=-1), dtype)
        n2 = xp.astype(_count_nonmasked(data2, axis=-1), dtype)
        cdf1 = xp.astype(_xp_searchsorted(data1, data_all, side='right'), dtype)
        cdf2 = xp.astype(_xp_searchsorted(data2, data_all, side='right'), dtype)
        cddiffs = cdf1/n1[..., xp.newaxis] - cdf2/n2[..., xp.newaxis]
        # but the switch from `xp.searchsorted` to `_xp_searchsorted` would come with a
        # pretty steep performance hit, so the algorithm below is faster.
        # When `xp.searchsorted` is vectorized, we can revert.
    else:
        n = n1 + n2

        # We want the ECDF of each sample evaluated at *all* the points in the pooled
        # sample. The values each ECDF can assume are given by:
        cdf1_vals = xp.broadcast_to(xp.linspace(0, 1, n1 + 1, dtype=dtype),
                                    batch_shape + (n1 + 1,))
        cdf2_vals = xp.broadcast_to(xp.linspace(0, 1, n2 + 1, dtype=dtype),
                                    batch_shape + (n2 + 1,))
        # Now we "just" need to know how many times each of these values *will* be
        # assumed when we evaluate the ECDFs at all points in the pooled sample.
        # These counts are given by the differences between consecutive ("min" or "max")
        # ranks corresponding with the observations in the (sorted) samples.
        ranks, data_all, _ = _rankdata(data_all, method='min', return_sorted=True)
        ranks = xp.astype(ranks, xp.asarray(1).dtype)  # default int type
        one = xp.ones((*ranks.shape[:-1], 1), dtype=ranks.dtype,
                      device=xp_device(ranks))
        cdf1_counts = xp.diff(ranks[..., :n1], prepend=one, append=n + one, axis=-1)
        cdf2_counts = xp.diff(ranks[..., -n2:], prepend=one, append=n + one, axis=-1)
        # Repeat isn't vectorized - in general, this would produce a ragged array.
        # However, in our case, the sum of repeats for each slice is the same, so we can
        # do a vectorized repeat by raveling, repeating, then restoring the shape.
        cdf1 = xp.repeat(xp_ravel(cdf1_vals), xp_ravel(cdf1_counts), axis=-1)
        cdf2 = xp.repeat(xp_ravel(cdf2_vals), xp_ravel(cdf2_counts), axis=-1)
        cddiffs = xp.reshape(cdf1 - cdf2, ranks.shape[:-1] + (-1,))

    # Identify the location of the statistic
    argminS = xp.argmin(cddiffs, axis=-1, keepdims=True)
    argmaxS = xp.argmax(cddiffs, axis=-1, keepdims=True)
    loc_minS = xp.squeeze(xp.take_along_axis(data_all, argminS, axis=-1), axis=-1)
    loc_maxS = xp.squeeze(xp.take_along_axis(data_all, argmaxS, axis=-1), axis=-1)

    # Ensure sign of minS is not negative.
    minS = -xp.squeeze(xp.take_along_axis(cddiffs, argminS, axis=-1), axis=-1)
    maxS = xp.squeeze(xp.take_along_axis(cddiffs, argmaxS, axis=-1), axis=-1)
    minS = xp.clip(minS, 0., 1.)

    if alternative == 'less':
        selector = xp.ones(minS.shape, dtype=xp.bool)
    elif alternative == 'two-sided':
        selector = minS > maxS
    else:
        selector = xp.zeros(minS.shape, dtype=xp.bool)

    d = xp.where(selector, minS, maxS)
    d_location = xp.where(selector, loc_minS, loc_maxS)
    one = xp.asarray(1, dtype=xp.int8)
    d_sign = xp.where(selector, -one, one)

    if is_marray(xp):
        d = d.data  # converted to NumPy below
        n1, n2 = np.asarray(n1.data, dtype=int), np.asarray(n2.data, dtype=int)
    prob = _ks_2samp_prob(np.asarray(d), n1, n2, mode, MAX_AUTO_N, alternative)
    dtype = xp_result_type(data1, data2, force_floating=True, xp=xp)
    prob = xp.asarray(prob, dtype=dtype)
    d = xp.asarray(d, dtype=dtype)
    if d.ndim == 0:
        d, prob, d_location, d_sign = d[()], prob[()], d_location[()], d_sign[()]
    return KstestResult(d, prob, statistic_location=d_location, statistic_sign=d_sign)

