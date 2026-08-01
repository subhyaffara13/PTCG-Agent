
def ks_1samp(x, cdf, args=(), alternative="two-sided", method='auto'):
    """
    Computes the Kolmogorov-Smirnov test on one sample of masked values.

    Missing values in `x` are discarded.

    Parameters
    ----------
    x : array_like
        a 1-D array of observations of random variables.
    cdf : str or callable
        If a string, it should be the name of a distribution in `scipy.stats`.
        If a callable, that callable is used to calculate the cdf.
    args : tuple, sequence, optional
        Distribution parameters, used if `cdf` is a string.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Indicates the alternative hypothesis.  Default is 'two-sided'.
    method : {'auto', 'exact', 'asymp'}, optional
        Defines the method used for calculating the p-value.
        The following options are available (default is 'auto'):

        * 'auto' : use 'exact' for small size arrays, 'asymp' for large
        * 'exact' : use approximation to exact distribution of test statistic
        * 'asymp' : use asymptotic distribution of test statistic

    Returns
    -------
    d : float
        Value of the Kolmogorov Smirnov test
    p : float
        Corresponding p-value.

    """
    alternative = {'t': 'two-sided', 'g': 'greater', 'l': 'less'}.get(
       alternative.lower()[0], alternative)
    return scipy.stats._stats_py.ks_1samp(
        x, cdf, args=args, alternative=alternative, method=method)


def ks_1samp(x, cdf, args=(), alternative='two-sided', method='auto', *, axis=0):
    """
    Performs the one-sample Kolmogorov-Smirnov test for goodness of fit.

    This test compares the underlying distribution F(x) of a sample
    against a given continuous distribution G(x). See Notes for a description
    of the available null and alternative hypotheses.

    Parameters
    ----------
    x : array_like
        a 1-D array of observations of iid random variables.
    cdf : callable
        callable used to calculate the cdf.
    args : tuple, sequence, optional
        Distribution parameters, used with `cdf`.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the null and alternative hypotheses. Default is 'two-sided'.
        Please see explanations in the Notes below.
    method : {'auto', 'exact', 'approx', 'asymp'}, optional
        Defines the distribution used for calculating the p-value.
        The following options are available (default is 'auto'):

        * 'auto' : selects one of the other options.
        * 'exact' : uses the exact distribution of test statistic.
        * 'approx' : approximates the two-sided probability with twice
          the one-sided probability
        * 'asymp': uses asymptotic distribution of test statistic

    axis : int or tuple of ints, default: 0
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    res: KstestResult
        An object containing attributes:

        statistic : float
            KS test statistic, either D+, D-, or D (the maximum of the two)
        pvalue : float
            One-tailed or two-tailed p-value.
        statistic_location : float
            Value of `x` corresponding with the KS statistic; i.e., the
            distance between the empirical distribution function and the
            hypothesized cumulative distribution function is measured at this
            observation.
        statistic_sign : int
            +1 if the KS statistic is the maximum positive difference between
            the empirical distribution function and the hypothesized cumulative
            distribution function (D+); -1 if the KS statistic is the maximum
            negative difference (D-).


    See Also
    --------
    ks_2samp, kstest

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
    >>> stats.ks_1samp(stats.uniform.rvs(size=100, random_state=rng),
    ...                stats.norm.cdf)
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
    >>> stats.ks_1samp(x, stats.norm.cdf)
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
    >>> stats.ks_1samp(x, stats.norm.cdf, alternative='less')
    KstestResult(statistic=0.17482387821055168,
                 pvalue=0.001913921057766743,
                 statistic_location=0.3713830565352756,
                 statistic_sign=-1)

    and indeed, with p-value smaller than our threshold, we reject the null
    hypothesis in favor of the alternative.

    """
    # `_axis_nan_policy` decorator ensures `axis=-1`
    xp = array_namespace(x)
    mode = method
    if mode not in ['auto', 'exact', 'approx', 'asymp']:
        raise ValueError(
            f"Invalid value for method: {mode!r}. "
            f"Must be one of 'auto', 'exact', 'approx', 'asymp'."
        )

    alternative = {'t': 'two-sided', 'g': 'greater', 'l': 'less'}.get(
        alternative.lower()[0], alternative)
    if alternative not in ['two-sided', 'greater', 'less']:
        raise ValueError(f"Unexpected value {alternative=}")

    x = xp.sort(x, axis=-1)
    x = xp_promote(x, force_floating=True, xp=xp)
    N = _count_nonmasked(x, axis=-1, xp=xp)
    cdfvals = _masked_apply(cdf, args=(x, *args), xp=xp)

    ones = xp.ones(x.shape[:-1], dtype=xp.int8)
    ones = ones[()] if ones.ndim == 0 else ones

    if alternative == 'greater':
        Dplus, d_location = _compute_d(cdfvals, x, +1)
        pvalue = _masked_apply(distributions.ksone.sf, args=(Dplus, N), xp=xp)
        pvalue = xp.asarray(pvalue, dtype=x.dtype)
        pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue
        Dplus = xp.asarray(Dplus) if is_marray(xp) else Dplus
        return KstestResult(Dplus, pvalue,
                            statistic_location=d_location,
                            statistic_sign=ones)

    if alternative == 'less':
        Dminus, d_location = _compute_d(cdfvals, x, -1)
        pvalue = _masked_apply(distributions.ksone.sf, args=(Dminus, N), xp=xp)
        pvalue = xp.asarray(pvalue, dtype=x.dtype)
        pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue
        Dminus = xp.asarray(Dminus) if is_marray(xp) else Dminus
        return KstestResult(Dminus, pvalue,
                            statistic_location=d_location,
                            statistic_sign=-ones)

    # alternative == 'two-sided':
    Dplus, dplus_location = _compute_d(cdfvals, x, +1)
    Dminus, dminus_location = _compute_d(cdfvals, x, -1)
    i_plus = Dplus > Dminus
    D = xp.where(i_plus, Dplus, Dminus)
    d_location = xp.where(i_plus, dplus_location, dminus_location)
    d_sign = xp.where(i_plus, ones, -ones)
    if D.ndim == 0:
        D, d_location, d_sign = D[()], d_location[()], d_sign[()]

    if mode == 'auto':  # Always select exact
        mode = 'exact'
    if mode == 'exact':
        prob = _masked_apply(distributions.kstwo.sf, args=(D, N), xp=xp)
    elif mode == 'asymp':
        prob = _masked_apply(distributions.kstwobign.sf, args=(D * N**0.5,), xp=xp)
    else:
        # mode == 'approx'
        prob = 2 * _masked_apply(distributions.ksone.sf, args=(D, N), xp=xp)
    prob = xp.clip(xp.asarray(prob, dtype=x.dtype), 0., 1.)
    return KstestResult(D, prob,
                        statistic_location=d_location,
                        statistic_sign=d_sign)

