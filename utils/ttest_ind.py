
def ttest_ind(a, b, axis=0, equal_var=True, alternative='two-sided'):
    """
    Calculates the T-test for the means of TWO INDEPENDENT samples of scores.

    Parameters
    ----------
    a, b : array_like
        The arrays must have the same shape, except in the dimension
        corresponding to `axis` (the first, by default).
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        arrays, `a`, and `b`.
    equal_var : bool, optional
        If True, perform a standard independent 2 sample test that assumes equal
        population variances.
        If False, perform Welch's t-test, which does not assume equal population
        variance.

        .. versionadded:: 0.17.0
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided': the means of the distributions underlying the samples
          are unequal.
        * 'less': the mean of the distribution underlying the first sample
          is less than the mean of the distribution underlying the second
          sample.
        * 'greater': the mean of the distribution underlying the first
          sample is greater than the mean of the distribution underlying
          the second sample.

        .. versionadded:: 1.7.0

    Returns
    -------
    statistic : float or array
        The calculated t-statistic.
    pvalue : float or array
        The p-value.

    Notes
    -----
    For more details on `ttest_ind`, see `scipy.stats.ttest_ind`.

    """
    a, b, axis = _chk2_asarray(a, b, axis)

    if a.size == 0 or b.size == 0:
        return Ttest_indResult(np.nan, np.nan)

    (x1, x2) = (a.mean(axis), b.mean(axis))
    (v1, v2) = (a.var(axis=axis, ddof=1), b.var(axis=axis, ddof=1))
    (n1, n2) = (a.count(axis), b.count(axis))

    if equal_var:
        # force df to be an array for masked division not to throw a warning
        df = ma.asanyarray(n1 + n2 - 2.0)
        svar = ((n1-1)*v1+(n2-1)*v2) / df
        denom = ma.sqrt(svar*(1.0/n1 + 1.0/n2))  # n-D computation here!
    else:
        vn1 = v1/n1
        vn2 = v2/n2
        with np.errstate(divide='ignore', invalid='ignore'):
            df = (vn1 + vn2)**2 / (vn1**2 / (n1 - 1) + vn2**2 / (n2 - 1))

        # If df is undefined, variances are zero.
        # It doesn't matter what df is as long as it is not NaN.
        df = np.where(np.isnan(df), 1, df)
        denom = ma.sqrt(vn1 + vn2)

    with np.errstate(divide='ignore', invalid='ignore'):
        t = (x1-x2) / denom

    t, prob = _ttest_finish(df, t, alternative)
    return Ttest_indResult(t, prob)


def ttest_ind(a, b, *, axis=0, equal_var=True, nan_policy='propagate',
              alternative="two-sided", trim=0, method=None):
    """
    Calculate the T-test for the means of *two independent* samples of scores.

    This is a test for the null hypothesis that 2 independent samples
    have identical average (expected) values. This test assumes that the
    populations have identical variances by default.

    Parameters
    ----------
    a, b : array_like
        The arrays must have the same shape, except in the dimension
        corresponding to `axis` (the first, by default).
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        arrays, `a`, and `b`.
    equal_var : bool, optional
        If True (default), perform a standard independent 2 sample test
        that assumes equal population variances [1]_.
        If False, perform Welch's t-test, which does not assume equal
        population variance [2]_.

        .. versionadded:: 0.11.0

    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

        The 'omit' option is not currently available for one-sided asymptotic tests.

    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided': the means of the distributions underlying the samples
          are unequal.
        * 'less': the mean of the distribution underlying the first sample
          is less than the mean of the distribution underlying the second
          sample.
        * 'greater': the mean of the distribution underlying the first
          sample is greater than the mean of the distribution underlying
          the second sample.

    trim : float, optional
        If nonzero, performs a trimmed (Yuen's) t-test.
        Defines the fraction of elements to be trimmed from each end of the
        input samples. If 0 (default), no elements will be trimmed from either
        side. The number of trimmed elements from each tail is the floor of the
        trim times the number of elements. Valid range is [0, .5).
    method : ResamplingMethod, optional
        Defines the method used to compute the p-value. If `method` is an
        instance of `PermutationMethod`/`MonteCarloMethod`, the p-value is
        computed using
        `scipy.stats.permutation_test`/`scipy.stats.monte_carlo_test` with the
        provided configuration options and other appropriate settings.
        Otherwise, the p-value is computed by comparing the test statistic
        against a theoretical t-distribution.

        .. versionadded:: 1.15.0

    Returns
    -------
    result : `~scipy.stats._result_classes.TtestResult`
        An object with the following attributes:

        statistic : float or ndarray
            The t-statistic.
        pvalue : float or ndarray
            The p-value associated with the given alternative.
        df : float or ndarray
            The number of degrees of freedom used in calculation of the
            t-statistic.

            .. versionadded:: 1.11.0

        The object also has the following method:

        confidence_interval(confidence_level=0.95)
            Computes a confidence interval around the difference in
            population means for the given confidence level.
            The confidence interval is returned in a ``namedtuple`` with
            fields ``low`` and ``high``.

            .. versionadded:: 1.11.0

    Notes
    -----
    Suppose we observe two independent samples, e.g. flower petal lengths, and
    we are considering whether the two samples were drawn from the same
    population (e.g. the same species of flower or two species with similar
    petal characteristics) or two different populations.

    The t-test quantifies the difference between the arithmetic means
    of the two samples. The p-value quantifies the probability of observing
    as or more extreme values assuming the null hypothesis, that the
    samples are drawn from populations with the same population means, is true.
    A p-value larger than a chosen threshold (e.g. 5% or 1%) indicates that
    our observation is not so unlikely to have occurred by chance. Therefore,
    we do not reject the null hypothesis of equal population means.
    If the p-value is smaller than our threshold, then we have evidence
    against the null hypothesis of equal population means.

    By default, the p-value is determined by comparing the t-statistic of the
    observed data against a theoretical t-distribution.

    It is also possible to compute the test statistic using a permutation test by
    passing ``method=scipy.stats.PermutationMethod(n_resamples=permutations)``,
    where ``permutations`` is the desired number of "permutations" to use in
    forming the null distribution. When ``1 < permutations < binom(n, k)``, where

    * ``k`` is the number of observations in `a`,
    * ``n`` is the total number of observations in `a` and `b`, and
    * ``binom(n, k)`` is the binomial coefficient (``n`` choose ``k``),

    the data are pooled (concatenated), randomly assigned to either group `a`
    or `b`, and the t-statistic is calculated. This process is performed
    repeatedly (``permutations`` times), generating a distribution of the
    t-statistic under the null hypothesis, and the t-statistic of the observed
    data is compared to this distribution to determine the p-value.
    Specifically, the p-value reported is the "achieved significance level"
    (ASL) as defined in 4.4 of [3]_. Note that there are other ways of
    estimating p-values using randomized permutation tests; for other
    options, see the more general `permutation_test`.

    When ``permutations >= binom(n, k)``, an exact test is performed: the data
    are partitioned between the groups in each distinct way exactly once.

    The permutation test can be computationally expensive and not necessarily
    more accurate than the analytical test, but it does not make strong
    assumptions about the shape of the underlying distribution.

    Use of trimming is commonly referred to as the trimmed t-test. At times
    called Yuen's t-test, this is an extension of Welch's t-test, with the
    difference being the use of winsorized means in calculation of the variance
    and the trimmed sample size in calculation of the statistic. Trimming is
    recommended if the underlying distribution is long-tailed or contaminated
    with outliers [4]_.

    The statistic is calculated as ``(np.mean(a) - np.mean(b))/se``, where
    ``se`` is the standard error. Therefore, the statistic will be positive
    when the sample mean of `a` is greater than the sample mean of `b` and
    negative when the sample mean of `a` is less than the sample mean of
    `b`.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/T-test#Independent_two-sample_t-test

    .. [2] https://en.wikipedia.org/wiki/Welch%27s_t-test

    .. [3] B. Efron and T. Hastie.
           Computer Age Statistical Inference. (2016).

    .. [4] Yuen, Karen K. "The Two-Sample Trimmed t for Unequal Population
           Variances." Biometrika, vol. 61, no. 1, 1974, pp. 165-170.
           https://www.jstor.org/stable/2334299

    .. [5] Yuen, Karen K., and W. J. Dixon. "The Approximate Behaviour and
           Performance of the Two-Sample Trimmed t." Biometrika, vol. 60,
           no. 2, 1973, pp. 369-374.
           https://www.jstor.org/stable/2334550

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()

    Test with sample with identical means:

    >>> rvs1 = stats.norm.rvs(loc=5, scale=10, size=500, random_state=rng)
    >>> rvs2 = stats.norm.rvs(loc=5, scale=10, size=500, random_state=rng)
    >>> stats.ttest_ind(rvs1, rvs2)
    TtestResult(statistic=-0.4390847099199348,
                pvalue=0.6606952038870015,
                df=998.0)
    >>> stats.ttest_ind(rvs1, rvs2, equal_var=False)
    TtestResult(statistic=-0.4390847099199348,
                pvalue=0.6606952553131064,
                df=997.4602304121448)

    `ttest_ind` underestimates p for unequal variances:

    >>> rvs3 = stats.norm.rvs(loc=5, scale=20, size=500, random_state=rng)
    >>> stats.ttest_ind(rvs1, rvs3)
    TtestResult(statistic=-1.6370984482905417,
                pvalue=0.1019251574705033,
                df=998.0)
    >>> stats.ttest_ind(rvs1, rvs3, equal_var=False)
    TtestResult(statistic=-1.637098448290542,
                pvalue=0.10202110497954867,
                df=765.1098655246868)

    When ``n1 != n2``, the equal variance t-statistic is no longer equal to the
    unequal variance t-statistic:

    >>> rvs4 = stats.norm.rvs(loc=5, scale=20, size=100, random_state=rng)
    >>> stats.ttest_ind(rvs1, rvs4)
    TtestResult(statistic=-1.9481646859513422,
                pvalue=0.05186270935842703,
                df=598.0)
    >>> stats.ttest_ind(rvs1, rvs4, equal_var=False)
    TtestResult(statistic=-1.3146566100751664,
                pvalue=0.1913495266513811,
                df=110.41349083985212)

    T-test with different means, variance, and n:

    >>> rvs5 = stats.norm.rvs(loc=8, scale=20, size=100, random_state=rng)
    >>> stats.ttest_ind(rvs1, rvs5)
    TtestResult(statistic=-2.8415950600298774,
                pvalue=0.0046418707568707885,
                df=598.0)
    >>> stats.ttest_ind(rvs1, rvs5, equal_var=False)
    TtestResult(statistic=-1.8686598649188084,
                pvalue=0.06434714193919686,
                df=109.32167496550137)

    Take these two samples, one of which has an extreme tail.

    >>> a = (56, 128.6, 12, 123.8, 64.34, 78, 763.3)
    >>> b = (1.1, 2.9, 4.2)

    Use the `trim` keyword to perform a trimmed (Yuen) t-test. For example,
    using 20% trimming, ``trim=.2``, the test will reduce the impact of one
    (``np.floor(trim*len(a))``) element from each tail of sample `a`. It will
    have no effect on sample `b` because ``np.floor(trim*len(b))`` is 0.

    >>> stats.ttest_ind(a, b, trim=.2)
    TtestResult(statistic=3.4463884028073513,
                pvalue=0.01369338726499547,
                df=6.0)
    """
    xp = array_namespace(a, b)

    a, b = xp_promote(a, b, force_floating=True, xp=xp)

    if axis is None:
        a, b, axis = xp_ravel(a), xp_ravel(b), 0

    if not (0 <= trim < .5):
        raise ValueError("Trimming percentage should be 0 <= `trim` < .5.")

    if not isinstance(method, PermutationMethod | MonteCarloMethod | None):
        message = ("`method` must be an instance of `PermutationMethod`, an instance "
                   "of `MonteCarloMethod`, or None (default).")
        raise ValueError(message)

    result_shape = _broadcast_array_shapes_remove_axis((a, b), axis=axis)
    NaN = _get_nan(a, b, shape=result_shape, xp=xp)
    if xp_size(a) == 0 or xp_size(b) == 0:
        return TtestResult(NaN, NaN, df=NaN, alternative=NaN,
                           standard_error=NaN, estimate=NaN)

    alternative_nums = {"less": -1, "two-sided": 0, "greater": 1}

    n1 = _count_nonmasked(a, axis)
    n2 = _count_nonmasked(b, axis)

    if trim == 0:
        with np.errstate(divide='ignore', invalid='ignore'):
            v1 = _var(a, axis, ddof=1, xp=xp)
            v2 = _var(b, axis, ddof=1, xp=xp)

        m1 = xp.mean(a, axis=axis)
        m2 = xp.mean(b, axis=axis)
    else:
        v1, m1, n1 = _ttest_trim_var_mean_len(a, trim, axis, xp=xp)
        v2, m2, n2 = _ttest_trim_var_mean_len(b, trim, axis, xp=xp)

    if equal_var:
        df, denom = _equal_var_ttest_denom(v1, n1, v2, n2, xp=xp)
    else:
        df, denom = _unequal_var_ttest_denom(v1, n1, v2, n2, xp=xp)

    if method is None:
        t, prob = _ttest_ind_from_stats(m1, m2, denom, df, alternative)
    else:
        # nan_policy is taken care of by axis_nan_policy decorator
        ttest_kwargs = dict(equal_var=equal_var, trim=trim)
        t, prob = _ttest_resampling(a, b, axis, alternative,
                                    ttest_kwargs, method, xp=xp)

    # when nan_policy='omit', `df` can be different for different axis-slices
    df = xp.broadcast_to(df, t.shape)
    df = df[()] if df.ndim ==0 else df
    estimate = m1 - m2

    return TtestResult(t, prob, df=df, alternative=alternative_nums[alternative],
                       standard_error=denom, estimate=estimate)

