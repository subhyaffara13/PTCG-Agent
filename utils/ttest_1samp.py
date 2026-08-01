
def ttest_1samp(a, popmean, axis=0, alternative='two-sided'):
    """
    Calculates the T-test for the mean of ONE group of scores.

    Parameters
    ----------
    a : array_like
        sample observation
    popmean : float or array_like
        expected value in null hypothesis, if array_like than it must have the
        same shape as `a` excluding the axis dimension
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        array `a`.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided': the mean of the underlying distribution of the sample
          is different than the given population mean (`popmean`)
        * 'less': the mean of the underlying distribution of the sample is
          less than the given population mean (`popmean`)
        * 'greater': the mean of the underlying distribution of the sample is
          greater than the given population mean (`popmean`)

        .. versionadded:: 1.7.0

    Returns
    -------
    statistic : float or array
        t-statistic
    pvalue : float or array
        The p-value

    Notes
    -----
    For more details on `ttest_1samp`, see `scipy.stats.ttest_1samp`.

    """
    a, axis = _chk_asarray(a, axis)
    if a.size == 0:
        return (np.nan, np.nan)

    x = a.mean(axis=axis)
    v = a.var(axis=axis, ddof=1)
    n = a.count(axis=axis)
    # force df to be an array for masked division not to throw a warning
    df = ma.asanyarray(n - 1.0)
    svar = ((n - 1.0) * v) / df
    with np.errstate(divide='ignore', invalid='ignore'):
        t = (x - popmean) / ma.sqrt(svar / n)

    t, prob = _ttest_finish(df, t, alternative)
    return Ttest_1sampResult(t, prob)


def ttest_1samp(a, popmean, axis=0, nan_policy="propagate", alternative="two-sided"):
    """Calculate the T-test for the mean of ONE group of scores.

    This is a test for the null hypothesis that the expected value
    (mean) of a sample of independent observations `a` is equal to the given
    population mean, `popmean`.

    Parameters
    ----------
    a : array_like
        Sample observations.
    popmean : float or array_like
        Expected value in null hypothesis. If array_like, then its length along
        `axis` must equal 1, and it must otherwise be broadcastable with `a`.
    axis : int or None, optional
        Axis along which to compute test; default is 0. If None, compute over
        the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided': the mean of the underlying distribution of the sample
          is different than the given population mean (`popmean`)
        * 'less': the mean of the underlying distribution of the sample is
          less than the given population mean (`popmean`)
        * 'greater': the mean of the underlying distribution of the sample is
          greater than the given population mean (`popmean`)

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
            Computes a confidence interval around the population
            mean for the given confidence level.
            The confidence interval is returned in a ``namedtuple`` with
            fields `low` and `high`.

            .. versionadded:: 1.10.0

    Notes
    -----
    The statistic is calculated as ``(np.mean(a) - popmean)/se``, where
    ``se`` is the standard error. Therefore, the statistic will be positive
    when the sample mean is greater than the population mean and negative when
    the sample mean is less than the population mean.

    Examples
    --------
    Suppose we wish to test the null hypothesis that the mean of a population
    is equal to 0.5. We choose a confidence level of 99%; that is, we will
    reject the null hypothesis in favor of the alternative if the p-value is
    less than 0.01.

    When testing random variates from the standard uniform distribution, which
    has a mean of 0.5, we expect the data to be consistent with the null
    hypothesis most of the time.

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> rvs = stats.uniform.rvs(size=50, random_state=rng)
    >>> stats.ttest_1samp(rvs, popmean=0.5)
    TtestResult(statistic=2.456308468440, pvalue=0.017628209047638, df=49)

    As expected, the p-value of 0.017 is not below our threshold of 0.01, so
    we cannot reject the null hypothesis.

    When testing data from the standard *normal* distribution, which has a mean
    of 0, we would expect the null hypothesis to be rejected.

    >>> rvs = stats.norm.rvs(size=50, random_state=rng)
    >>> stats.ttest_1samp(rvs, popmean=0.5)
    TtestResult(statistic=-7.433605518875, pvalue=1.416760157221e-09, df=49)

    Indeed, the p-value is lower than our threshold of 0.01, so we reject the
    null hypothesis in favor of the default "two-sided" alternative: the mean
    of the population is *not* equal to 0.5.

    However, suppose we were to test the null hypothesis against the
    one-sided alternative that the mean of the population is *greater* than
    0.5. Since the mean of the standard normal is less than 0.5, we would not
    expect the null hypothesis to be rejected.

    >>> stats.ttest_1samp(rvs, popmean=0.5, alternative='greater')
    TtestResult(statistic=-7.433605518875, pvalue=0.99999999929, df=49)

    Unsurprisingly, with a p-value greater than our threshold, we would not
    reject the null hypothesis.

    Note that when working with a confidence level of 99%, a true null
    hypothesis will be rejected approximately 1% of the time.

    >>> rvs = stats.uniform.rvs(size=(100, 50), random_state=rng)
    >>> res = stats.ttest_1samp(rvs, popmean=0.5, axis=1)
    >>> np.sum(res.pvalue < 0.01)
    1

    Indeed, even though all 100 samples above were drawn from the standard
    uniform distribution, which *does* have a population mean of 0.5, we would
    mistakenly reject the null hypothesis for one of them.

    `ttest_1samp` can also compute a confidence interval around the population
    mean.

    >>> rvs = stats.norm.rvs(size=50, random_state=rng)
    >>> res = stats.ttest_1samp(rvs, popmean=0)
    >>> ci = res.confidence_interval(confidence_level=0.95)
    >>> ci
    ConfidenceInterval(low=-0.3193887540880017, high=0.2898583388980972)

    The bounds of the 95% confidence interval are the
    minimum and maximum values of the parameter `popmean` for which the
    p-value of the test would be 0.05.

    >>> res = stats.ttest_1samp(rvs, popmean=ci.low)
    >>> np.testing.assert_allclose(res.pvalue, 0.05)
    >>> res = stats.ttest_1samp(rvs, popmean=ci.high)
    >>> np.testing.assert_allclose(res.pvalue, 0.05)

    Under certain assumptions about the population from which a sample
    is drawn, the confidence interval with confidence level 95% is expected
    to contain the true population mean in 95% of sample replications.

    >>> rvs = stats.norm.rvs(size=(50, 1000), loc=1, random_state=rng)
    >>> res = stats.ttest_1samp(rvs, popmean=0)
    >>> ci = res.confidence_interval()
    >>> contains_pop_mean = (ci.low < 1) & (ci.high > 1)
    >>> contains_pop_mean.sum()
    953

    """
    xp = array_namespace(a)
    a, popmean = xp_promote(a, popmean, force_floating=True, xp=xp)
    a, axis = _chk_asarray(a, axis, xp=xp)

    n = _count_nonmasked(a, axis)
    df = n - 1

    if a.shape[axis] == 0:
        # This is really only needed for *testing* _axis_nan_policy decorator
        # It won't happen when the decorator is used.
        NaN = _get_nan(a)
        return TtestResult(NaN, NaN, df=NaN, alternative=NaN,
                           standard_error=NaN, estimate=NaN)

    mean = xp.mean(a, axis=axis)
    try:
        popmean = xp.asarray(popmean)
        popmean = xp.squeeze(popmean, axis=axis) if popmean.ndim > 0 else popmean
    except ValueError as e:
        raise ValueError("`popmean.shape[axis]` must equal 1.") from e
    d = mean - popmean
    v = _var(a, axis=axis, ddof=1)
    denom = xp.sqrt(v / n)

    with np.errstate(divide='ignore', invalid='ignore'):
        t = xp.divide(d, denom)
        t = t[()] if t.ndim == 0 else t

    dist = _SimpleStudentT(xp.asarray(df, dtype=t.dtype, device=xp_device(a)))
    prob = _get_pvalue(t, dist, alternative, xp=xp)
    prob = prob[()] if prob.ndim == 0 else prob

    # when nan_policy='omit', `df` can be different for different axis-slices
    df = xp.broadcast_to(xp.asarray(df, device=xp_device(a)), t.shape)
    df = df[()] if df.ndim == 0 else df
    # _axis_nan_policy decorator doesn't play well with strings
    alternative_num = {"less": -1, "two-sided": 0, "greater": 1}[alternative]
    return TtestResult(t, prob, df=df, alternative=alternative_num,
                       standard_error=denom, estimate=mean,
                       statistic_np=xp.asarray(t), xp=xp)

