
def kstest(data1, data2, args=(), alternative='two-sided', method='auto'):
    """
    Performs the Kolmogorov-Smirnov test for goodness of fit.

    Parameters
    ----------
    data1 : array_like
    data2 : str, callable or array_like
    args : tuple, sequence, optional
        Distribution parameters, used if `data1` or `data2` are strings.
    alternative : str, as documented in stats.kstest
    method : str, as documented in stats.kstest

    Returns
    -------
    tuple of (K-S statistic, probability)

    """  # numpydoc ignore=RT03
    return scipy.stats._stats_py.kstest(data1, data2, args,
                                        alternative=alternative, method=method)


def kstest(rvs, cdf, args=(), N=20, alternative='two-sided', method='auto', *,
           axis=0):
    """
    Performs the (one-sample or two-sample) Kolmogorov-Smirnov test for
    goodness of fit.

    The one-sample test compares the underlying distribution F(x) of a sample
    against a given distribution G(x). The two-sample test compares the
    underlying distributions of two independent samples. Both tests are valid
    only for continuous distributions.

    Parameters
    ----------
    rvs : str, array_like, or callable
        If an array, it should be a 1-D array of observations of random
        variables.
        If a callable, it should be a function to generate random variables;
        it is required to have a keyword argument `size`.
        If a string, it should be the name of a distribution in `scipy.stats`,
        which will be used to generate random variables.
    cdf : str, array_like or callable
        If array_like, it should be a 1-D array of observations of random
        variables, and the two-sample test is performed
        (and rvs must be array_like).
        If a callable, that callable is used to calculate the cdf.
        If a string, it should be the name of a distribution in `scipy.stats`,
        which will be used as the cdf function.
    args : tuple, sequence, optional
        Distribution parameters, used if `rvs` or `cdf` are strings or
        callables.
    N : int, optional
        Sample size if `rvs` is string or callable.  Default is 20.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the null and alternative hypotheses. Default is 'two-sided'.
        Please see explanations in the Notes below.
    method : {'auto', 'exact', 'approx', 'asymp'}, optional
        Defines the distribution used for calculating the p-value.
        The following options are available (default is 'auto'):

        * 'auto' : selects one of the other options.
        * 'exact' : uses the exact distribution of test statistic.
        * 'approx' : approximates the two-sided probability with twice the
          one-sided probability
        * 'asymp': uses asymptotic distribution of test statistic

    Returns
    -------
    res: KstestResult
        An object containing attributes:

        statistic : float
            KS test statistic, either D+, D-, or D (the maximum of the two)
        pvalue : float
            One-tailed or two-tailed p-value.
        statistic_location : float
            In a one-sample test, this is the value of `rvs`
            corresponding with the KS statistic; i.e., the distance between
            the empirical distribution function and the hypothesized cumulative
            distribution function is measured at this observation.

            In a two-sample test, this is the value from `rvs` or `cdf`
            corresponding with the KS statistic; i.e., the distance between
            the empirical distribution functions is measured at this
            observation.
        statistic_sign : int
            In a one-sample test, this is +1 if the KS statistic is the
            maximum positive difference between the empirical distribution
            function and the hypothesized cumulative distribution function
            (D+); it is -1 if the KS statistic is the maximum negative
            difference (D-).

            In a two-sample test, this is +1 if the empirical distribution
            function of `rvs` exceeds the empirical distribution
            function of `cdf` at `statistic_location`, otherwise -1.

    See Also
    --------
    ks_1samp, ks_2samp

    Notes
    -----
    There are three options for the null and corresponding alternative
    hypothesis that can be selected using the `alternative` parameter.

    - `two-sided`: The null hypothesis is that the two distributions are
      identical, F(x)=G(x) for all x; the alternative is that they are not
      identical.

    - `less`: The null hypothesis is that F(x) >= G(x) for all x; the
      alternative is that F(x) < G(x) for at least one x.

    - `greater`: The null hypothesis is that F(x) <= G(x) for all x; the
      alternative is that F(x) > G(x) for at least one x.

    Note that the alternative hypotheses describe the *CDFs* of the
    underlying distributions, not the observed values. For example,
    suppose x1 ~ F and x2 ~ G. If F(x) > G(x) for all x, the values in
    x1 tend to be less than those in x2.


    Examples
    --------
    Suppose we wish to test the null hypothesis that a sample is distributed
    according to the standard normal.
    We choose a confidence level of 95%; that is, we will reject the null
    hypothesis in favor of the alternative if the p-value is less than 0.05.

    When testing uniformly distributed data, we would expect the
    null hypothesis to be rejected.

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> stats.kstest(stats.uniform.rvs(size=100, random_state=rng),
    ...              stats.norm.cdf)
    KstestResult(statistic=0.5001899973268688,
                 pvalue=1.1616392184763533e-23,
                 statistic_location=0.00047625268963724654,
                 statistic_sign=-1)

    Indeed, the p-value is lower than our threshold of 0.05, so we reject the
    null hypothesis in favor of the default "two-sided" alternative: the data
    are *not* distributed according to the standard normal.

    When testing random variates from the standard normal distribution, we
    expect the data to be consistent with the null hypothesis most of the time.

    >>> x = stats.norm.rvs(size=100, random_state=rng)
    >>> stats.kstest(x, stats.norm.cdf)
    KstestResult(statistic=0.05345882212970396,
                 pvalue=0.9227159037744717,
                 statistic_location=-1.2451343873745018,
                 statistic_sign=1)


    As expected, the p-value of 0.92 is not below our threshold of 0.05, so
    we cannot reject the null hypothesis.

    Suppose, however, that the random variates are distributed according to
    a normal distribution that is shifted toward greater values. In this case,
    the cumulative density function (CDF) of the underlying distribution tends
    to be *less* than the CDF of the standard normal. Therefore, we would
    expect the null hypothesis to be rejected with ``alternative='less'``:

    >>> x = stats.norm.rvs(size=100, loc=0.5, random_state=rng)
    >>> stats.kstest(x, stats.norm.cdf, alternative='less')
    KstestResult(statistic=0.17482387821055168,
                 pvalue=0.001913921057766743,
                 statistic_location=0.3713830565352756,
                 statistic_sign=-1)

    and indeed, with p-value smaller than our threshold, we reject the null
    hypothesis in favor of the alternative.

    For convenience, the previous test can be performed using the name of the
    distribution as the second argument.

    >>> stats.kstest(x, "norm", alternative='less')
    KstestResult(statistic=0.17482387821055168,
                 pvalue=0.001913921057766743,
                 statistic_location=0.3713830565352756,
                 statistic_sign=-1)

    The examples above have all been one-sample tests identical to those
    performed by `ks_1samp`. Note that `kstest` can also perform two-sample
    tests identical to those performed by `ks_2samp`. For example, when two
    samples are drawn from the same distribution, we expect the data to be
    consistent with the null hypothesis most of the time.

    >>> sample1 = stats.laplace.rvs(size=105, random_state=rng)
    >>> sample2 = stats.laplace.rvs(size=95, random_state=rng)
    >>> stats.kstest(sample1, sample2)
    KstestResult(statistic=0.11779448621553884,
                 pvalue=0.4494256912629795,
                 statistic_location=0.6138814275424155,
                 statistic_sign=1)

    As expected, the p-value of 0.45 is not below our threshold of 0.05, so
    we cannot reject the null hypothesis.

    """
    # to not break compatibility with existing code
    if alternative == 'two_sided':
        alternative = 'two-sided'
    if alternative not in ['two-sided', 'greater', 'less']:
        raise ValueError(f"Unexpected alternative: {alternative}")
    xvals, yvals, cdf = _parse_kstest_args(rvs, cdf, args, N)
    if cdf:
        return ks_1samp(xvals, cdf, args=args, alternative=alternative,
                        method=method, axis=axis, _no_deco=True)
    return ks_2samp(xvals, yvals, alternative=alternative, method=method,
                    axis=axis, _no_deco=True)

