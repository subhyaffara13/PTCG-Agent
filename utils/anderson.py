
def anderson(x, dist='norm', *, method=None):
    """Anderson-Darling test for data coming from a particular distribution.

    The Anderson-Darling test tests the null hypothesis that a sample is
    drawn from a population that follows a particular distribution.
    For the Anderson-Darling test, the critical values depend on
    which distribution is being tested against.  This function works
    for normal, exponential, logistic, weibull_min, or Gumbel (Extreme Value
    Type I) distributions.

    Parameters
    ----------
    x : array_like
        Array of sample data.
    dist : {'norm', 'expon', 'logistic', 'gumbel', 'gumbel_l', 'gumbel_r', 'extreme1', 'weibull_min'}, optional
        The type of distribution to test against.  The default is 'norm'.
        The names 'extreme1', 'gumbel_l' and 'gumbel' are synonyms for the
        same distribution.
    method : str or instance of `MonteCarloMethod`
        Defines the method used to compute the p-value.
        If `method` is ``"interpolated"``, the p-value is interpolated from
        pre-calculated tables.
        If `method` is an instance of `MonteCarloMethod`, the p-value is computed using
        `scipy.stats.monte_carlo_test` with the provided configuration options and other
        appropriate settings.

        .. versionadded:: 1.17.0
            If `method` is not specified, `anderson` will emit a ``FutureWarning``
            specifying that the user must opt into a p-value calculation method.
            When `method` is specified, the object returned will include a ``pvalue``
            attribute, but no ``critical_value``, ``significance_level``, or
            ``fit_result`` attributes. Beginning in 1.19.0, these other attributes will
            no longer be available, and a p-value will always be computed according to
            one of the available `method` options.

    Returns
    -------
    result : AndersonResult
        If `method` is provided, this is an object with the following attributes:

        statistic : float
            The Anderson-Darling test statistic.
        pvalue: float
            The p-value corresponding with the test statistic, calculated according to
            the specified `method`.

        If `method` is unspecified, this is an object with the following attributes:

        statistic : float
            The Anderson-Darling test statistic.
        critical_values : list
            The critical values for this distribution.
        significance_level : list
            The significance levels for the corresponding critical values
            in percents.  The function returns critical values for a
            differing set of significance levels depending on the
            distribution that is being tested against.
        fit_result : `~scipy.stats._result_classes.FitResult`
            An object containing the results of fitting the distribution to
            the data.

        .. deprecated:: 1.17.0
            The tuple-unpacking behavior of the return object and attributes
            ``critical_values``, ``significance_level``, and ``fit_result`` are
            deprecated. Beginning in SciPy 1.19.0, these features will no longer be
            available, and the object returned will have attributes ``statistic`` and
            ``pvalue``.

    See Also
    --------
    kstest : The Kolmogorov-Smirnov test for goodness-of-fit.

    Notes
    -----
    Critical values provided when `method` is unspecified are for the following
    significance levels:

    normal/exponential
        15%, 10%, 5%, 2.5%, 1%
    logistic
        25%, 10%, 5%, 2.5%, 1%, 0.5%
    gumbel_l / gumbel_r
        25%, 10%, 5%, 2.5%, 1%
    weibull_min
        50%, 25%, 15%, 10%, 5%, 2.5%, 1%, 0.5%

    If the returned statistic is larger than these critical values then
    for the corresponding significance level, the null hypothesis that
    the data come from the chosen distribution can be rejected.
    The returned statistic is referred to as 'A2' in the references.

    For `weibull_min`, maximum likelihood estimation is known to be
    challenging. If the test returns successfully, then the first order
    conditions for a maximum likelihood estimate have been verified and
    the critical values correspond relatively well to the significance levels,
    provided that the sample is sufficiently large (>10 observations [7]).
    However, for some data - especially data with no left tail - `anderson`
    is likely to result in an error message. In this case, consider
    performing a custom goodness of fit test using
    `scipy.stats.monte_carlo_test`.

    References
    ----------
    .. [1] https://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm
    .. [2] Stephens, M. A. (1974). EDF Statistics for Goodness of Fit and
           Some Comparisons, Journal of the American Statistical Association,
           Vol. 69, pp. 730-737.
    .. [3] Stephens, M. A. (1976). Asymptotic Results for Goodness-of-Fit
           Statistics with Unknown Parameters, Annals of Statistics, Vol. 4,
           pp. 357-369.
    .. [4] Stephens, M. A. (1977). Goodness of Fit for the Extreme Value
           Distribution, Biometrika, Vol. 64, pp. 583-588.
    .. [5] Stephens, M. A. (1977). Goodness of Fit with Special Reference
           to Tests for Exponentiality , Technical Report No. 262,
           Department of Statistics, Stanford University, Stanford, CA.
    .. [6] Stephens, M. A. (1979). Tests of Fit for the Logistic Distribution
           Based on the Empirical Distribution Function, Biometrika, Vol. 66,
           pp. 591-595.
    .. [7] Richard A. Lockhart and Michael A. Stephens "Estimation and Tests of
           Fit for the Three-Parameter Weibull Distribution"
           Journal of the Royal Statistical Society.Series B(Methodological)
           Vol. 56, No. 3 (1994), pp. 491-500, Table 0.
    .. [8] D'Agostino, Ralph B. (1986). "Tests for the Normal Distribution".
           In: Goodness-of-Fit Techniques. Ed. by Ralph B. D'Agostino and
           Michael A. Stephens. New York: Marcel Dekker, pp. 122-141. ISBN:
           0-8247-7487-6.

    Examples
    --------
    Test the null hypothesis that a random sample was drawn from a normal
    distribution (with unspecified mean and standard deviation).

    >>> import numpy as np
    >>> from scipy.stats import anderson
    >>> rng = np.random.default_rng(9781234521)
    >>> data = rng.random(size=35)
    >>> res = anderson(data, dist='norm', method='interpolate')
    >>> res.statistic
    np.float64(0.9887620209957291)
    >>> res.pvalue
    np.float64(0.012111200538380142)

    The p-value is approximately 0.012,, so the null hypothesis may be rejected
    at a significance level of 2.5%, but not at a significance level of 1%.

    """ # numpy/numpydoc#87  # noqa: E501
    dist = dist.lower()
    if dist in {'extreme1', 'gumbel'}:
        dist = 'gumbel_l'
    dists = {'norm', 'expon', 'gumbel_l',
             'gumbel_r', 'logistic', 'weibull_min'}

    if dist not in dists:
        raise ValueError(f"Invalid distribution; dist must be in {dists}.")
    y = sort(x)
    xbar = np.mean(x, axis=0)
    N = len(y)
    if dist == 'norm':
        s = np.std(x, ddof=1, axis=0)
        w = (y - xbar) / s
        fit_params = xbar, s
        logcdf = distributions.norm.logcdf(w)
        logsf = distributions.norm.logsf(w)
        sig = array([15, 10, 5, 2.5, 1])
        critical = around(_Avals_norm / (1.0 + 0.75/N + 2.25/N/N), 3)
    elif dist == 'expon':
        w = y / xbar
        fit_params = 0, xbar
        logcdf = distributions.expon.logcdf(w)
        logsf = distributions.expon.logsf(w)
        sig = array([15, 10, 5, 2.5, 1])
        critical = around(_Avals_expon / (1.0 + 0.6/N), 3)
    elif dist == 'logistic':
        def rootfunc(ab, xj, N):
            a, b = ab
            tmp = (xj - a) / b
            tmp2 = exp(tmp)
            val = [np.sum(1.0/(1+tmp2), axis=0) - 0.5*N,
                   np.sum(tmp*(1.0-tmp2)/(1+tmp2), axis=0) + N]
            return array(val)

        sol0 = array([xbar, np.std(x, ddof=1, axis=0)])
        sol = optimize.fsolve(rootfunc, sol0, args=(x, N), xtol=1e-5)
        w = (y - sol[0]) / sol[1]
        fit_params = sol
        logcdf = distributions.logistic.logcdf(w)
        logsf = distributions.logistic.logsf(w)
        sig = array([25, 10, 5, 2.5, 1, 0.5])
        critical = around(_Avals_logistic / (1.0 + 0.25/N), 3)
    elif dist == 'gumbel_r':
        xbar, s = distributions.gumbel_r.fit(x)
        w = (y - xbar) / s
        fit_params = xbar, s
        logcdf = distributions.gumbel_r.logcdf(w)
        logsf = distributions.gumbel_r.logsf(w)
        sig = array([25, 10, 5, 2.5, 1])
        critical = around(_Avals_gumbel / (1.0 + 0.2/sqrt(N)), 3)
    elif dist == 'gumbel_l':
        xbar, s = distributions.gumbel_l.fit(x)
        w = (y - xbar) / s
        fit_params = xbar, s
        logcdf = distributions.gumbel_l.logcdf(w)
        logsf = distributions.gumbel_l.logsf(w)
        sig = array([25, 10, 5, 2.5, 1])
        critical = around(_Avals_gumbel / (1.0 + 0.2/sqrt(N)), 3)
    elif dist == 'weibull_min':
        message = ("Critical values of the test statistic are given for the "
                   "asymptotic distribution. These may not be accurate for "
                   "samples with fewer than 10 observations. Consider using "
                   "`scipy.stats.monte_carlo_test`.")
        if N < 10:
            warnings.warn(message, stacklevel=2)
        # [7] writes our 'c' as 'm', and they write `c = 1/m`. Use their names.
        m, loc, scale = distributions.weibull_min.fit(y)
        m, loc, scale = _weibull_fit_check((m, loc, scale), y)
        fit_params = m, loc, scale
        logcdf = stats.weibull_min(*fit_params).logcdf(y)
        logsf = stats.weibull_min(*fit_params).logsf(y)
        c = 1 / m  # m and c are as used in [7]
        sig = array([0.5, 0.75, 0.85, 0.9, 0.95, 0.975, 0.99, 0.995])
        critical = _get_As_weibull(c)
        # Goodness-of-fit tests should only be used to provide evidence
        # _against_ the null hypothesis. Be conservative and round up.
        critical = np.round(critical + 0.0005, decimals=3)

    i = arange(1, N + 1)
    A2 = -N - np.sum((2*i - 1.0) / N * (logcdf + logsf[::-1]), axis=0)

    # FitResult initializer expects an optimize result, so let's work with it
    message = '`anderson` successfully fit the distribution to the data.'
    res = optimize.OptimizeResult(success=True, message=message)
    res.x = np.array(fit_params)
    fit_result = FitResult(getattr(distributions, dist), y,
                           discrete=False, res=res)

    if method is None:
        warnings.warn(_anderson_warning_message, FutureWarning, stacklevel=2)
        return AndersonResult(A2, critical, sig, fit_result=fit_result)

    if method == 'interpolate':
        sig = 1 - sig if dist == 'weibull_min' else sig / 100
        pvalue = np.interp(A2, critical, sig)
    elif isinstance(method, stats.MonteCarloMethod):
        pvalue = _anderson_simulate_pvalue(x, dist, method)
    else:
        message = ("`method` must be either 'interpolate' or "
                   "an instance of `MonteCarloMethod`.")
        raise ValueError(message)
    return SignificanceResult(statistic=A2, pvalue=pvalue)


def Anderson(*args, **kwargs):
    """
    1d-solver generating pairs of approximative root and error.

    Uses Anderson-Bjoerk method to find a root of f in [a, b].
    Wrapper for illinois to use method='pegasus'.
    """
    kwargs['method'] = 'anderson'
    return Illinois(*args, **kwargs)

