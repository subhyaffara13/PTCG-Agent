
def kruskal(*samples):
    """
    Compute the Kruskal-Wallis H-test for independent samples

    Parameters
    ----------
    *samples : array_like
       Two or more arrays with the sample measurements can be given as
       arguments.

    Returns
    -------
    statistic : float
       The Kruskal-Wallis H statistic, corrected for ties
    pvalue : float
       The p-value for the test using the assumption that H has a chi
       square distribution

    Notes
    -----
    For more details on `kruskal`, see `scipy.stats.kruskal`.

    Examples
    --------
    >>> from scipy.stats.mstats import kruskal

    Random samples from three different brands of batteries were tested
    to see how long the charge lasted. Results were as follows:

    >>> a = [6.3, 5.4, 5.7, 5.2, 5.0]
    >>> b = [6.9, 7.0, 6.1, 7.9]
    >>> c = [7.2, 6.9, 6.1, 6.5]

    Test the hypothesis that the distribution functions for all of the brands'
    durations are identical. Use 5% level of significance.

    >>> kruskal(a, b, c)
    KruskalResult(statistic=7.113812154696133, pvalue=0.028526948491942164)

    The null hypothesis is rejected at the 5% level of significance
    because the returned p-value is less than the critical value of 5%.

    """
    output = argstoarray(*samples)
    ranks = ma.masked_equal(rankdata(output, use_missing=False), 0)
    sumrk = ranks.sum(-1)
    ngrp = ranks.count(-1)
    ntot = ranks.count()
    H = 12./(ntot*(ntot+1)) * (sumrk**2/ngrp).sum() - 3*(ntot+1)
    # Tie correction
    ties = count_tied_groups(ranks)
    T = 1. - sum(v*(k**3-k) for (k,v) in ties.items())/float(ntot**3-ntot)
    if T == 0:
        raise ValueError('All numbers are identical in kruskal')

    H /= T
    df = len(output) - 1
    prob = distributions.chi2.sf(H, df)
    return KruskalResult(H, prob)


def kruskal(*samples, nan_policy='propagate', axis=0):
    """Compute the Kruskal-Wallis H-test for independent samples.

    The Kruskal-Wallis H-test tests the null hypothesis that the population
    median of all of the groups are equal.  It is a non-parametric version of
    ANOVA.  The test works on 2 or more independent samples, which may have
    different sizes.  Note that rejecting the null hypothesis does not
    indicate which of the groups differs.  Post hoc comparisons between
    groups are required to determine which groups are different.

    Parameters
    ----------
    *samples : array_like
       Two or more arrays with the sample measurements can be given as
       arguments. Samples must be one-dimensional.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    axis : int or tuple of ints, default: 0
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    statistic : float
       The Kruskal-Wallis H statistic, corrected for ties.
    pvalue : float
       The p-value for the test using the assumption that H has a chi
       square distribution. The p-value returned is the survival function of
       the chi square distribution evaluated at H.

    See Also
    --------
    f_oneway : 1-way ANOVA.
    mannwhitneyu : Mann-Whitney rank test on two samples.
    friedmanchisquare : Friedman test for repeated measurements.

    Notes
    -----
    Due to the assumption that H has a chi square distribution, the number
    of samples in each group must not be too small.  A typical rule is
    that each sample must have at least 5 measurements.

    References
    ----------
    .. [1] W. H. Kruskal & W. W. Wallis, "Use of Ranks in
       One-Criterion Variance Analysis", Journal of the American Statistical
       Association, Vol. 47, Issue 260, pp. 583-621, 1952.
    .. [2] https://en.wikipedia.org/wiki/Kruskal-Wallis_one-way_analysis_of_variance

    Examples
    --------
    >>> from scipy import stats
    >>> x = [1, 3, 5, 7, 9]
    >>> y = [2, 4, 6, 8, 10]
    >>> stats.kruskal(x, y)
    KruskalResult(statistic=0.2727272727272734, pvalue=0.6015081344405895)

    >>> x = [1, 1, 1]
    >>> y = [2, 2, 2]
    >>> z = [2, 2]
    >>> stats.kruskal(x, y, z)
    KruskalResult(statistic=7.0, pvalue=0.0301973834223185)

    """
    xp = array_namespace(*samples)
    samples = xp_promote(*samples, force_floating=True, xp=xp)

    num_groups = len(samples)
    if num_groups < 2:
        raise ValueError("Need at least two groups in stats.kruskal()")

    lengths = [sample.shape[-1] for sample in samples]
    if any(lengths) < 1:  # Only needed for `test_axis_nan_policy`
        raise ValueError("Inputs must not be empty.")

    alldata = xp.concat(samples, axis=-1)
    ranked, _, t = _rankdata(alldata, method='average', return_ties=True)
    counts = [xp.asarray(_count_nonmasked(sample, -1), dtype=t.dtype)
              for sample in samples]
    totaln = sum(counts)
    ties = 1 - xp.sum(t**3 - t, axis=-1) / (totaln**3 - totaln)  # tiecorrect(ranked)

    # Compute sum^2/count for each group and sum
    j = list(itertools.accumulate(lengths, initial=0))
    ssbn = sum(xp.sum(ranked[..., j[i]:j[i + 1]], axis=-1)**2 / counts[i]
               for i in range(num_groups))

    h = 12.0 / (totaln * (totaln + 1)) * ssbn - 3 * (totaln + 1)
    df = xp.asarray(num_groups - 1, dtype=h.dtype)
    h /= ties

    chi2 = _SimpleChi2(df)
    pvalue = _get_pvalue(h, chi2, alternative='greater', symmetric=False, xp=np)
    return KruskalResult(h, pvalue)

