
def ttest_rel(a, b, axis=0, alternative='two-sided'):
    """
    Calculates the T-test on TWO RELATED samples of scores, a and b.

    Parameters
    ----------
    a, b : array_like
        The arrays must have the same shape.
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        arrays, `a`, and `b`.
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
        t-statistic
    pvalue : float or array
        two-tailed p-value

    Notes
    -----
    For more details on `ttest_rel`, see `scipy.stats.ttest_rel`.

    """
    a, b, axis = _chk2_asarray(a, b, axis)
    if len(a) != len(b):
        raise ValueError('unequal length arrays')

    if a.size == 0 or b.size == 0:
        return Ttest_relResult(np.nan, np.nan)

    n = a.count(axis)
    df = ma.asanyarray(n-1.0)
    d = (a-b).astype('d')
    dm = d.mean(axis)
    v = d.var(axis=axis, ddof=1)
    denom = ma.sqrt(v / n)
    with np.errstate(divide='ignore', invalid='ignore'):
        t = dm / denom

    t, prob = _ttest_finish(df, t, alternative)
    return Ttest_relResult(t, prob)


def ttest_rel(a, b, axis=0, nan_policy='propagate', alternative="two-sided"):
    """Calculate the t-test on TWO RELATED samples of scores, a and b.

    This is a test for the null hypothesis that two related or
    repeated samples have identical average (expected) values.

    Parameters
    ----------
    a, b : array_like
        The arrays must have the same shape.
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        arrays, `a`, and `b`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

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

        .. versionadded:: 1.6.0

    Returns
    -------
    result : `~scipy.stats._result_classes.TtestResult`
        An object with the following attributes:

        statistic : float or array
            The t-statistic.
        pvalue : float or array
            The p-value associated with the given alternative.
        df : float or array
            The number of degrees of freedom used in calculation of the
            t-statistic; this is one less than the size of the sample
            (``a.shape[axis]``).

            .. versionadded:: 1.10.0

        The object also has the following method:

        confidence_interval(confidence_level=0.95)
            Computes a confidence interval around the difference in
            population means for the given confidence level.
            The confidence interval is returned in a ``namedtuple`` with
            fields `low` and `high`.

            .. versionadded:: 1.10.0

    Notes
    -----
    Examples for use are scores of the same set of student in
    different exams, or repeated sampling from the same units. The
    test measures whether the average score differs significantly
    across samples (e.g. exams). If we observe a large p-value, for
    example greater than 0.05 or 0.1 then we cannot reject the null
    hypothesis of identical average scores. If the p-value is smaller
    than the threshold, e.g. 1%, 5% or 10%, then we reject the null
    hypothesis of equal averages. Small p-values are associated with
    large t-statistics.

    The t-statistic is calculated as ``np.mean(a - b)/se``, where ``se`` is the
    standard error. Therefore, the t-statistic will be positive when the sample
    mean of ``a - b`` is greater than zero and negative when the sample mean of
    ``a - b`` is less than zero.

    References
    ----------
    https://en.wikipedia.org/wiki/T-test#Dependent_t-test_for_paired_samples

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()

    >>> rvs1 = stats.norm.rvs(loc=5, scale=10, size=500, random_state=rng)
    >>> rvs2 = (stats.norm.rvs(loc=5, scale=10, size=500, random_state=rng)
    ...         + stats.norm.rvs(scale=0.2, size=500, random_state=rng))
    >>> stats.ttest_rel(rvs1, rvs2)
    TtestResult(statistic=-0.4549717054410304, pvalue=0.6493274702088672, df=499)
    >>> rvs3 = (stats.norm.rvs(loc=8, scale=10, size=500, random_state=rng)
    ...         + stats.norm.rvs(scale=0.2, size=500, random_state=rng))
    >>> stats.ttest_rel(rvs1, rvs3)
    TtestResult(statistic=-5.879467544540889, pvalue=7.540777129099917e-09, df=499)

    """
    return ttest_1samp(a - b, popmean=0., axis=axis, alternative=alternative,
                       _no_deco=True)

