
def friedmanchisquare(*args):
    """Friedman Chi-Square is a non-parametric, one-way within-subjects ANOVA.
    This function calculates the Friedman Chi-square test for repeated measures
    and returns the result, along with the associated probability value.

    Each input is considered a given group. Ideally, the number of treatments
    among each group should be equal. If this is not the case, only the first
    n treatments are taken into account, where n is the number of treatments
    of the smallest group.
    If a group has some missing values, the corresponding treatments are masked
    in the other groups.
    The test statistic is corrected for ties.

    Masked values in one group are propagated to the other groups.

    Returns
    -------
    statistic : float
        the test statistic.
    pvalue : float
        the associated p-value.

    """
    data = argstoarray(*args).astype(float)
    k = len(data)
    if k < 3:
        raise ValueError(f"Less than 3 groups ({k}): the Friedman test "
                         f"is NOT appropriate.")

    ranked = ma.masked_values(rankdata(data, axis=0), 0)
    if ranked._mask is not nomask:
        ranked = ma.mask_cols(ranked)
        ranked = ranked.compressed().reshape(k,-1).view(ndarray)
    else:
        ranked = ranked._data
    (k,n) = ranked.shape
    # Ties correction
    repeats = [find_repeats(row) for row in ranked.T]
    ties = np.array([y for x, y in repeats if x.size > 0])
    tie_correction = 1 - (ties**3-ties).sum()/float(n*(k**3-k))

    ssbg = np.sum((ranked.sum(-1) - n*(k+1)/2.)**2)
    chisq = ssbg * 12./(n*k*(k+1)) * 1./tie_correction

    return FriedmanchisquareResult(chisq,
                                   distributions.chi2.sf(chisq, k-1))


def friedmanchisquare(*samples, axis=0):
    """Compute the Friedman test for repeated samples.

    The Friedman test tests the null hypothesis that repeated samples of
    the same individuals have the same distribution.  It is often used
    to test for consistency among samples obtained in different ways.
    For example, if two sampling techniques are used on the same set of
    individuals, the Friedman test can be used to determine if the two
    sampling techniques are consistent.

    Parameters
    ----------
    *samples : array_like
        Arrays of observations.  All of the arrays must have the same number
        of elements.  At least three samples must be given.
    axis : int or tuple of ints, default: 0
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    statistic : float
        The test statistic, correcting for ties.
    pvalue : float
        The associated p-value assuming that the test statistic has a chi
        squared distribution.

    See Also
    --------
    :ref:`hypothesis_friedmanchisquare` : Extended example

    Notes
    -----
    Due to the assumption that the test statistic has a chi squared
    distribution, the p-value is only reliable for n > 10 and more than
    6 repeated samples.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Friedman_test
    .. [2] Demsar, J. (2006). Statistical comparisons of classifiers over
           multiple data sets. Journal of Machine Learning Research, 7, 1-30.

    Examples
    --------

    >>> import numpy as np
    >>> rng = np.random.default_rng(seed=18)
    >>> x = rng.random((6, 10))
    >>> from scipy.stats import friedmanchisquare
    >>> res = friedmanchisquare(x[0], x[1], x[2], x[3], x[4], x[5])
    >>> res.statistic, res.pvalue
    (11.428571428571416, 0.043514520866727614)

    The p-value is less than 0.05; however, as noted above, the results may not
    be reliable since we have a small number of repeated samples.

    For a more detailed example, see :ref:`hypothesis_friedmanchisquare`.
    """
    k = len(samples)
    if k < 3:
        raise ValueError('At least 3 samples must be given '
                         f'for Friedman test, got {k}.')

    xp = array_namespace(*samples)
    samples = xp_promote(*samples, force_floating=True, xp=xp)
    dtype = samples[0].dtype
    samples = _share_masks(*samples, xp=xp)  # paired-sample test

    n = samples[0].shape[-1]
    if n == 0:  # only for `test_axis_nan_policy`; user doesn't see this
        raise ValueError("One or more sample arguments is too small.")

    # Rank data
    # axis-slices are aligned with axis -1 by decorator; stack puts samples along axis 0
    # The transpose flips this so we can work with axis-slices along -1. This is a
    # reducing statistic, so both axes 0 and -1 are consumed.
    data = xp_swapaxes(xp.stack(samples), 0, -1)
    data, _, t = _rankdata(data, method='average', return_ties=True)

    # Handle ties
    ties = xp.sum(t * (t*t - 1), axis=(0, -1))
    count = xp.asarray(_count_nonmasked(samples[0], axis=-1), dtype=ties.dtype)
    c = 1 - ties / (k*(k*k - 1)*count)

    ssbn = xp.sum(xp.sum(data, axis=0)**2, axis=-1)
    statistic = (12.0 / (k*count*(k+1)) * ssbn - 3*count*(k+1)) / c

    chi2 = _SimpleChi2(xp.asarray(k - 1, dtype=dtype))
    pvalue = _get_pvalue(statistic, chi2, alternative='greater', symmetric=False, xp=xp)
    return FriedmanchisquareResult(statistic, pvalue)

