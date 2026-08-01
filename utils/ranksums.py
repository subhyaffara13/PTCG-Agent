
def ranksums(x, y, alternative='two-sided'):
    """Compute the Wilcoxon rank-sum statistic for two samples.

    .. legacy:: function

        This function includes a subset of the features of `mannwhitneyu`.
        Its statistic and p-value can be reproduced using `mannwhitneyu` with
        options ``use_continuity=False`` and ``method='asymptotic'``.
        Prefer `mannwhitneyu` for use in new code.

    The Wilcoxon rank-sum test tests the null hypothesis that two sets
    of measurements are drawn from the same distribution.  The alternative
    hypothesis is that values in one sample are more likely to be
    larger than the values in the other sample.

    This test should be used to compare two samples from continuous
    distributions.  It does not handle ties between measurements
    in x and y.  For tie-handling and an optional continuity correction
    see `scipy.stats.mannwhitneyu`.

    Parameters
    ----------
    x, y : array_like
        The data from the two samples.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': one of the distributions (underlying `x` or `y`) is
          stochastically greater than the other.
        * 'less': the distribution underlying `x` is stochastically less
          than the distribution underlying `y`.
        * 'greater': the distribution underlying `x` is stochastically greater
          than the distribution underlying `y`.

        .. versionadded:: 1.7.0

    Returns
    -------
    statistic : float
        The test statistic under the large-sample approximation that the
        rank sum statistic is normally distributed.
    pvalue : float
        The p-value of the test.

    See Also
    --------
    scipy.stats.mannwhitneyu

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Wilcoxon_rank-sum_test

    Examples
    --------
    We can test the hypothesis that two independent unequal-sized samples are
    drawn from the same distribution with computing the Wilcoxon rank-sum
    statistic.

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng(6004253334)
    >>> sample1 = rng.uniform(-1, 1, 200)
    >>> sample2 = rng.uniform(-0.5, 1.5, 300) # a shifted distribution
    >>> stats.ranksums(sample1, sample2)
    RanksumsResult(statistic=np.float64(-7.576201867),
                   pvalue=np.float64(3.5581802537469756e-14))
    >>> stats.ranksums(sample1, sample2, alternative='less')
    RanksumsResult(statistic=np.float64(-7.576201867066302),
                   pvalue=np.float64(1.7790901268734878e-14))
    >>> stats.ranksums(sample1, sample2, alternative='greater')
    RanksumsResult(statistic=np.float64(-7.576201867066302),
                   pvalue=np.float64(0.9999999999999822))

    The p-value of less than ``0.05`` indicates that this test rejects the
    hypothesis at the 5% significance level.

    Note that identical hypothesis tests (and more accurate ones) can be performed
    using `mannwhitneyu`. Prefer `mannwhitneyu` for use in new code.

    >>> res = stats.mannwhitneyu(sample1, sample2, alternative='greater',
    ...                          method='asymptotic', use_continuity = False)
    >>> res.zstatistic
    np.float64(-7.576201867066302)
    >>> res.pvalue
    np.float64(0.9999999999999822)
    """
    x, y = map(np.asarray, (x, y))
    n1 = len(x)
    n2 = len(y)
    alldata = np.concatenate((x, y))
    ranked = rankdata(alldata)
    x = ranked[:n1]
    s = np.sum(x, axis=0)
    expected = n1 * (n1+n2+1) / 2.0
    z = (s - expected) / np.sqrt(n1*n2*(n1+n2+1)/12.0)
    pvalue = _get_pvalue(z, _SimpleNormal(), alternative, xp=np)

    return RanksumsResult(z[()], pvalue[()])

