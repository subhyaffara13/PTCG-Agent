
def binomtest(k, n, p=0.5, alternative='two-sided'):
    """
    Perform a test that the probability of success is p.

    The binomial test [1]_ is a test of the null hypothesis that the
    probability of success in a Bernoulli experiment is `p`.

    Details of the test can be found in many texts on statistics, such
    as section 24.5 of [2]_.

    The documentation is written as though the function accepts and returns Python
    scalars, but the function is vectorized to work elementwise with NumPy arrays.

    Parameters
    ----------
    k : int
        The number of successes.
    n : int
        The number of trials.
    p : float, optional
        The hypothesized probability of success, i.e. the expected
        proportion of successes.  The value must be in the interval
        ``0 <= p <= 1``. The default value is ``p = 0.5``.
    alternative : {'two-sided', 'greater', 'less'}, optional
        Indicates the alternative hypothesis. The default value is
        'two-sided'.

    Returns
    -------
    result : `~scipy.stats._result_classes.BinomTestResult` instance
        The return value is an object with the following attributes:

        k : int
            The number of successes (copied from `binomtest` input).
        n : int
            The number of trials (copied from `binomtest` input).
        alternative : str
            Indicates the alternative hypothesis specified in the input
            to `binomtest`.  It will be one of ``'two-sided'``, ``'greater'``,
            or ``'less'``.
        statistic : float
            The estimate of the proportion of successes.
        pvalue : float
            The p-value of the hypothesis test.

        The object has the following methods:

        proportion_ci(confidence_level=0.95, method='exact') :
            Compute the confidence interval for ``statistic``.

    Notes
    -----
    .. versionadded:: 1.7.0

    References
    ----------
    .. [1] Binomial test, https://en.wikipedia.org/wiki/Binomial_test
    .. [2] Jerrold H. Zar, Biostatistical Analysis (fifth edition),
           Prentice Hall, Upper Saddle River, New Jersey USA (2010)

    Examples
    --------
    >>> from scipy.stats import binomtest

    A car manufacturer claims that no more than 10% of their cars are unsafe.
    15 cars are inspected for safety, 3 were found to be unsafe. Test the
    manufacturer's claim:

    >>> result = binomtest(3, n=15, p=0.1, alternative='greater')
    >>> result.pvalue
    0.18406106910639114

    The null hypothesis cannot be rejected at the 5% level of significance
    because the returned p-value is greater than the critical value of 5%.

    The test statistic is equal to the estimated proportion, which is simply
    ``3/15``:

    >>> result.statistic
    0.2

    We can use the `proportion_ci()` method of the result to compute the
    confidence interval of the estimate:

    >>> result.proportion_ci(confidence_level=0.95)
    ConfidenceInterval(low=0.05684686759024681, high=1.0)

    """
    xp = array_namespace(k, n, p)
    k, n, p = xp_promote(k, n, p, force_floating=True, broadcast=True, xp=xp)
    k_valid = (k >= 0) & (k <= n) & (k == xp.floor(k))
    n_valid = (n >= 1) & (n == xp.floor(n))
    p_valid = (p >= 0) & (p <= 1)
    valid = k_valid & n_valid & p_valid
    k = xp.where(valid, k, xp.nan)
    n = xp.where(valid, n, xp.nan)
    p = xp.where(valid, p, xp.nan)

    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError(f"alternative ('{alternative}') not recognized; \n"
                         "must be 'two-sided', 'less' or 'greater'")

    B = _SimpleBinomial(n, p)
    if alternative == 'less':
        pval = B.cdf(k)
    elif alternative == 'greater':
        pval = B.sf(k - 1)
    else:
        if is_jax(xp):
            message = "`alternative='two-sided'` is incompatible with JAX arrays."
            raise ValueError(message)

        # alternative is 'two-sided'
        d = B.pmf(k)
        rerr = 1 + 1e-7

        def k_lt_pn(d, k, p, n):
            B = _SimpleBinomial(n, p)
            ix = _binary_search_for_binom_tst(lambda x1: -B.pmf(x1), -d*rerr,
                                              xp.ceil(p * n), n, xp=xp)
            # y is the number of terms between mode and n that are <= d*rerr.
            # ix gave us the first term where a(ix) <= d*rerr < a(ix-1)
            # if the first equality doesn't hold, y=n-ix. Otherwise, we
            # need to include ix as well as the equality holds. Note that
            # the equality will hold in very very rare situations due to rerr.
            y = n - ix + xp.asarray(d*rerr == B.pmf(ix), dtype=ix.dtype)
            pval = B.cdf(k) + B.sf(n - y)
            return pval

        def k_gte_pn(d, k, p, n):
            B = _SimpleBinomial(n, p)
            ix = _binary_search_for_binom_tst(B.pmf, d*rerr,
                                              xp.zeros_like(n), xp.floor(p * n), xp=xp)
            # y is the number of terms between 0 and mode that are <= d*rerr.
            # we need to add a 1 to account for the 0 index.
            # For comparing this with old behavior, see
            # tst_binary_srch_for_binom_tst method in test_morestats.
            y = ix + 1
            pval = B.cdf(y-1) + B.sf(k-1)
            return pval

        pval = xpx.apply_where(k < p*n, (d, k, p, n), k_lt_pn,  k_gte_pn)
        # xp.minimum(1.0, pval) but for data-apis/array-api-compat#271
        pval = xp.minimum(xp.asarray(1.0, dtype=pval.dtype), pval)

    statistic = xp.where(valid, k/n, xp.nan)
    pval = xp.where(valid, pval, xp.nan)
    if statistic.ndim == 0:
        k, n, statistic, pval = k[()], n[()], statistic[()], pval[()]

    result = BinomTestResult(k=k, n=n, alternative=alternative,
                             statistic=statistic, pvalue=pval, xp=xp)
    return result

