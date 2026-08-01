
def ansari(x, y, alternative='two-sided', *, axis=0, method='auto'):
    """Perform the Ansari-Bradley test for equal scale parameters.

    The Ansari-Bradley test ([1]_, [2]_) is a non-parametric test
    for the equality of the scale parameter of the distributions
    from which two samples were drawn. The null hypothesis states that
    the ratio of the scale of the distribution underlying `x` to the scale
    of the distribution underlying `y` is 1.

    Parameters
    ----------
    x, y : array_like
        Arrays of sample data.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Default is 'two-sided'.
        The following options are available:

        * 'two-sided': the ratio of scales is not equal to 1.
        * 'less': the ratio of scales is less than 1.
        * 'greater': the ratio of scales is greater than 1.

        .. versionadded:: 1.7.0
    axis : int or tuple of ints, default: 0
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.
    method : {'auto', 'asymptotic', 'exact'} or `PermutationMethod` instance, optional
        Selects the method used to calculate the *p*-value.
        Default is 'auto'. The following options are available.

        * ``'asymptotic'``: compares the standardized test statistic
          against the normal distribution, correcting for ties.
        * ``'exact'``: computes the exact *p*-value by comparing the observed
          statistic against the exact distribution of the statistic under the
          null hypothesis. No correction is made for ties.
        * ``'auto'``: chooses ``'exact'`` when the size of both
          samples is less than or equal to 55 and there are no ties;
          chooses ``'asymptotic'`` otherwise.
        * `PermutationMethod` instance. In this case, the p-value
          is computed using `permutation_test` with the provided
          configuration options and other appropriate settings.

    Returns
    -------
    statistic : float
        The Ansari-Bradley test statistic.
    pvalue : float
        The p-value of the hypothesis test.

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    mood : A non-parametric test for the equality of two scale parameters

    Notes
    -----
    The p-value given is exact when the sample sizes are both less than
    55 and there are no ties, otherwise a normal approximation for the
    p-value is used.

    References
    ----------
    .. [1] Ansari, A. R. and Bradley, R. A. (1960) Rank-sum tests for
           dispersions, Annals of Mathematical Statistics, 31, 1174-1189.
    .. [2] Sprent, Peter and N.C. Smeeton.  Applied nonparametric
           statistical methods.  3rd ed. Chapman and Hall/CRC. 2001.
           Section 5.8.2.
    .. [3] Nathaniel E. Helwig "Nonparametric Dispersion and Equality
           Tests" at http://users.stat.umn.edu/~helwig/notes/npde-Notes.pdf

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import ansari
    >>> rng = np.random.default_rng()

    For these examples, we'll create three random data sets.  The first
    two, with sizes 35 and 25, are drawn from a normal distribution with
    mean 0 and standard deviation 2.  The third data set has size 25 and
    is drawn from a normal distribution with standard deviation 1.25.

    >>> x1 = rng.normal(loc=0, scale=2, size=35)
    >>> x2 = rng.normal(loc=0, scale=2, size=25)
    >>> x3 = rng.normal(loc=0, scale=1.25, size=25)

    First we apply `ansari` to `x1` and `x2`.  These samples are drawn
    from the same distribution, so we expect the Ansari-Bradley test
    should not lead us to conclude that the scales of the distributions
    are different.

    >>> ansari(x1, x2)
    AnsariResult(statistic=541.0, pvalue=0.9762532927399098)

    With a p-value close to 1, we cannot conclude that there is a
    significant difference in the scales (as expected).

    Now apply the test to `x1` and `x3`:

    >>> ansari(x1, x3)
    AnsariResult(statistic=425.0, pvalue=0.0003087020407974518)

    The probability of observing such an extreme value of the statistic
    under the null hypothesis of equal scales is only 0.03087%. We take this
    as evidence against the null hypothesis in favor of the alternative:
    the scales of the distributions from which the samples were drawn
    are not equal.

    We can use the `alternative` parameter to perform a one-tailed test.
    In the above example, the scale of `x1` is greater than `x3` and so
    the ratio of scales of `x1` and `x3` is greater than 1. This means
    that the p-value when ``alternative='greater'`` should be near 0 and
    hence we should be able to reject the null hypothesis:

    >>> ansari(x1, x3, alternative='greater')
    AnsariResult(statistic=425.0, pvalue=0.0001543510203987259)

    As we can see, the p-value is indeed quite low. Use of
    ``alternative='less'`` should thus yield a large p-value:

    >>> ansari(x1, x3, alternative='less')
    AnsariResult(statistic=425.0, pvalue=0.9998643258449039)

    """
    xp = array_namespace(x, y)
    dtype = xp_result_type(x, y, force_floating=True, xp=xp)

    if alternative not in {'two-sided', 'greater', 'less'}:
        raise ValueError("'alternative' must be 'two-sided',"
                         " 'greater', or 'less'.")
    methods = {'auto', 'asymptotic', 'exact'}
    if str(method) not in methods and not isinstance(method, stats.PermutationMethod):
        message = (f"`method` must be one of {methods} or "
                   "an instance of `PermutationMethod`.")
        raise ValueError(message)
    if is_lazy_array(x) and method == 'auto':
        message = ("`method` must be 'exact', 'asymptotic', or an instance of "
                   "`PermutationMethod` when used with lazy arrays.")
        raise ValueError(message)

    if not hasattr(_abw_state, 'a'):
        _abw_state.a = _ABW()

    # _axis_nan_policy decorator guarantees that axis=-1
    n = x.shape[-1]
    m = y.shape[-1]
    if m < 1:  # needed by test_axis_nan_policy; not user-facing
        raise ValueError("Not enough other observations.")
    if n < 1:
        raise ValueError("Not enough test observations.")

    N = m + n
    xy = xp.concat([x, y], axis=-1)  # combine
    rank, _, t = _stats_py._rankdata(xy, method='average', return_ties=True)
    symrank = xp.minimum(rank, N - rank + 1)
    AB = xp.sum(symrank[..., :n], axis=-1)
    repeats = xp.any(t > 1)  # in theory we could branch for each slice separately

    if method == "auto":
        method = 'exact' if ((m < 55) and (n < 55) and not repeats) else 'asymptotic'

    if method == 'exact':
        # np.vectorize converts to NumPy here, and we convert back to the result
        # type before returning
        cdf = np.vectorize(_abw_state.a.cdf, otypes=[np.float64])
        sf = np.vectorize(_abw_state.a.sf, otypes=[np.float64])
        def get_ansari_pvalue(AB):
            if alternative == 'two-sided':
                pval = 2.0 * np.minimum(cdf(AB, n, m), sf(AB, n, m))
            elif alternative == 'greater':
                # AB statistic is _smaller_ when ratio of scales is larger,
                # so this is the opposite of the usual calculation
                pval = cdf(AB, n, m)
            else:
                pval = sf(AB, n, m)
            return pval

        pval = xpx.lazy_apply(get_ansari_pvalue, AB, shape=AB.shape)
        pval = xp.clip(xp.asarray(pval, dtype=dtype), max=1.0)
        AB = AB[()] if AB.ndim == 0 else AB
        pval = pval[()] if pval.ndim == 0 else pval
        return AnsariResult(AB, pval)

    elif isinstance(method, stats.PermutationMethod):
        def statistic(x, y, axis):
            return ansari(x, y, axis=axis, method="asymptotic").statistic
        alternative = dict(less='greater', greater='less').get(alternative, 'two-sided')
        res = stats.permutation_test((x, y), statistic, axis=axis,
                                     **method._asdict(), alternative=alternative)
        return AnsariResult(AB, res.pvalue)

    mnAB = (n * (N + 1.0) ** 2 / 4.0 / N) if N % 2 else (n * (N + 2.0) / 4.0)

    if is_lazy_array(repeats) or repeats:   # adjust variance estimates
        # compute np.sum(tj * rj**2,axis=0)
        fac = xp.sum(symrank**2, axis=-1)
        if N % 2:  # N odd
            varAB = m * n * (16*N*fac - (N+1)**4) / (16.0 * N**2 * (N-1))
        else:  # N even
            varAB = m * n * (16*fac - N*(N+2)**2) / (16.0 * N * (N-1))
    else:
        # otherwise compute normal approximation
        if N % 2:  # N odd
            varAB = n * m * (N + 1.0) * (3 + N ** 2) / (48.0 * N ** 2)
        else:
            varAB = m * n * (N + 2) * (N - 2.0) / 48 / (N - 1.0)
        varAB = xp.asarray(varAB, dtype=dtype)

    # Small values of AB indicate larger dispersion for the x sample.
    # Large values of AB indicate larger dispersion for the y sample.
    # This is opposite to the way we define the ratio of scales. see [1]_.
    z = (mnAB - AB) / xp.sqrt(varAB)
    pvalue = _get_pvalue(z, _SimpleNormal(), alternative, xp=xp)
    AB = AB[()] if AB.ndim == 0 else AB
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue
    return AnsariResult(AB, pvalue)

