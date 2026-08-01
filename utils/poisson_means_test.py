
def poisson_means_test(k1, n1, k2, n2, *, diff=0, alternative='two-sided'):
    r"""
    Performs the Poisson means test, AKA the "E-test".

    This is a test of the null hypothesis that the difference between means of
    two Poisson distributions is `diff`. The samples are provided as the
    number of events `k1` and `k2` observed within measurement intervals
    (e.g. of time, space, number of observations) of sizes `n1` and `n2`.

    Parameters
    ----------
    k1 : int
        Number of events observed from distribution 1.
    n1 : float
        Size of sample from distribution 1.
    k2 : int
        Number of events observed from distribution 2.
    n2 : float
        Size of sample from distribution 2.
    diff : float, default=0
        The hypothesized difference in means between the distributions
        underlying the samples.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided': the difference between distribution means is not
          equal to `diff`
        * 'less': the difference between distribution means is less than
          `diff`
        * 'greater': the difference between distribution means is greater
          than `diff`

    Returns
    -------
    statistic : float
        The test statistic (see [1]_ equation 3.3).
    pvalue : float
        The probability of achieving such an extreme value of the test
        statistic under the null hypothesis.

    Notes
    -----

    Let:

    .. math:: X_1 \sim \mbox{Poisson}(\mathtt{n1}\lambda_1)

    be a random variable independent of

    .. math:: X_2  \sim \mbox{Poisson}(\mathtt{n2}\lambda_2)

    and let ``k1`` and ``k2`` be the observed values of :math:`X_1`
    and :math:`X_2`, respectively. Then `poisson_means_test` uses the number
    of observed events ``k1`` and ``k2`` from samples of size ``n1`` and
    ``n2``, respectively, to test the null hypothesis that

    .. math::
       H_0: \lambda_1 - \lambda_2 = \mathtt{diff}

    A benefit of the E-test is that it has good power for small sample sizes,
    which can reduce sampling costs [1]_. It has been evaluated and determined
    to be more powerful than the comparable C-test, sometimes referred to as
    the Poisson exact test.

    References
    ----------
    .. [1]  Krishnamoorthy, K., & Thomson, J. (2004). A more powerful test for
       comparing two Poisson means. Journal of Statistical Planning and
       Inference, 119(1), 23-35.

    .. [2]  Przyborowski, J., & Wilenski, H. (1940). Homogeneity of results in
       testing samples from Poisson series: With an application to testing
       clover seed for dodder. Biometrika, 31(3/4), 313-323.

    Examples
    --------

    Suppose that a gardener wishes to test the number of dodder (weed) seeds
    in a sack of clover seeds that they buy from a seed company. It has
    previously been established that the number of dodder seeds in clover
    follows the Poisson distribution.

    A 100 gram sample is drawn from the sack before being shipped to the
    gardener. The sample is analyzed, and it is found to contain no dodder
    seeds; that is, `k1` is 0. However, upon arrival, the gardener draws
    another 100 gram sample from the sack. This time, three dodder seeds are
    found in the sample; that is, `k2` is 3. The gardener would like to
    know if the difference is significant and not due to chance. The
    null hypothesis is that the difference between the two samples is merely
    due to chance, or that :math:`\lambda_1 - \lambda_2 = \mathtt{diff}`
    where :math:`\mathtt{diff} = 0`. The alternative hypothesis is that the
    difference is not due to chance, or :math:`\lambda_1 - \lambda_2 \ne 0`.
    The gardener selects a significance level of 5% to reject the null
    hypothesis in favor of the alternative [2]_.

    >>> import scipy.stats as stats
    >>> res = stats.poisson_means_test(0, 100, 3, 100)
    >>> res.statistic, res.pvalue
    (-1.7320508075688772, 0.08837900929018157)

    The p-value is .088, indicating a near 9% chance of observing a value of
    the test statistic under the null hypothesis. This exceeds 5%, so the
    gardener does not reject the null hypothesis as the difference cannot be
    regarded as significant at this level.
    """

    _poisson_means_test_iv(k1, n1, k2, n2, diff, alternative)

    # "for a given k_1 and k_2, an estimate of \lambda_2 is given by" [1] (3.4)
    lmbd_hat2 = ((k1 + k2) / (n1 + n2) - diff * n1 / (n1 + n2))

    # "\hat{\lambda_{2k}} may be less than or equal to zero ... and in this
    # case the null hypothesis cannot be rejected ... [and] it is not necessary
    # to compute the p-value". [1] page 26 below eq. (3.6).
    if lmbd_hat2 <= 0:
        return _stats_py.SignificanceResult(0, 1)

    # The unbiased variance estimate [1] (3.2)
    var = k1 / (n1 ** 2) + k2 / (n2 ** 2)

    # The _observed_ pivot statistic from the input. It follows the
    # unnumbered equation following equation (3.3) This is used later in
    # comparison with the computed pivot statistics in an indicator function.
    t_k1k2 = (k1 / n1 - k2 / n2 - diff) / np.sqrt(var)

    # Equation (3.5) of [1] is lengthy, so it is broken into several parts,
    # beginning here. Note that the probability mass function of poisson is
    # exp^(-\mu)*\mu^k/k!, so and this is called with shape \mu, here noted
    # here as nlmbd_hat*. The strategy for evaluating the double summation in
    # (3.5) is to create two arrays of the values of the two products inside
    # the summation and then broadcast them together into a matrix, and then
    # sum across the entire matrix.

    # Compute constants (as seen in the first and second separated products in
    # (3.5).). (This is the shape (\mu) parameter of the poisson distribution.)
    nlmbd_hat1 = n1 * (lmbd_hat2 + diff)
    nlmbd_hat2 = n2 * lmbd_hat2

    # Determine summation bounds for tail ends of distribution rather than
    # summing to infinity. `x1*` is for the outer sum and `x2*` is the inner
    # sum.
    x1_lb, x1_ub = distributions.poisson.ppf([1e-10, 1 - 1e-16], nlmbd_hat1)
    x2_lb, x2_ub = distributions.poisson.ppf([1e-10, 1 - 1e-16], nlmbd_hat2)

    # Construct arrays to function as the x_1 and x_2 counters on the summation
    # in (3.5). `x1` is in columns and `x2` is in rows to allow for
    # broadcasting.
    x1 = np.arange(x1_lb, x1_ub + 1)
    x2 = np.arange(x2_lb, x2_ub + 1)[:, None]

    # These are the two products in equation (3.5) with `prob_x1` being the
    # first (left side) and `prob_x2` being the second (right side). (To
    # make as clear as possible: the 1st contains a "+ d" term, the 2nd does
    # not.)
    prob_x1 = distributions.poisson.pmf(x1, nlmbd_hat1)
    prob_x2 = distributions.poisson.pmf(x2, nlmbd_hat2)

    # compute constants for use in the "pivot statistic" per the
    # unnumbered equation following (3.3).
    lmbd_x1 = x1 / n1
    lmbd_x2 = x2 / n2
    lmbds_diff = lmbd_x1 - lmbd_x2 - diff
    var_x1x2 = lmbd_x1 / n1 + lmbd_x2 / n2

    # This is the 'pivot statistic' for use in the indicator of the summation
    # (left side of "I[.]").
    with np.errstate(invalid='ignore', divide='ignore'):
        t_x1x2 = lmbds_diff / np.sqrt(var_x1x2)

    # `[indicator]` implements the "I[.] ... the indicator function" per
    # the paragraph following equation (3.5).
    if alternative == 'two-sided':
        indicator = np.abs(t_x1x2) >= np.abs(t_k1k2)
    elif alternative == 'less':
        indicator = t_x1x2 <= t_k1k2
    else:
        indicator = t_x1x2 >= t_k1k2

    # Multiply all combinations of the products together, exclude terms
    # based on the `indicator` and then sum. (3.5)
    pvalue = np.sum((prob_x1 * prob_x2)[indicator])
    return _stats_py.SignificanceResult(t_k1k2, pvalue)

