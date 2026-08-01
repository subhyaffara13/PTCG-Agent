
def jarque_bera(x, *, axis=None):
    r"""Perform the Jarque-Bera goodness of fit test on sample data.

    The Jarque-Bera test tests whether the sample data has the skewness and
    kurtosis matching a normal distribution.

    Note that this test only works for a large enough number of data samples
    (>2000) as the test statistic asymptotically has a Chi-squared distribution
    with 2 degrees of freedom.

    Parameters
    ----------
    x : array_like
        Observations of a random variable.
    axis : int or None, default: 0
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear in
        a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    result : SignificanceResult
        An object with the following attributes:

        statistic : float
            The test statistic.
        pvalue : float
            The p-value for the hypothesis test.

    See Also
    --------
    :ref:`hypothesis_jarque_bera` : Extended example

    References
    ----------
    .. [1] Jarque, C. and Bera, A. (1980) "Efficient tests for normality,
           homoscedasticity and serial independence of regression residuals",
           6 Econometric Letters 255-259.

    Examples
    --------

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> x = rng.normal(0, 1, 100000)
    >>> jarque_bera_test = stats.jarque_bera(x)
    >>> jarque_bera_test
    Jarque_beraResult(statistic=3.3415184718131554, pvalue=0.18810419594996775)
    >>> jarque_bera_test.statistic
    3.3415184718131554
    >>> jarque_bera_test.pvalue
    0.18810419594996775

    For a more detailed example, see :ref:`hypothesis_jarque_bera`.
    """
    xp = array_namespace(x)
    x, axis = _chk_asarray(x, axis, xp=xp)

    mu = _xp_mean(x, axis=axis, keepdims=True)
    diffx = x - mu
    s = skew(diffx, axis=axis, _no_deco=True)
    k = kurtosis(diffx, axis=axis, _no_deco=True)

    n = xp.asarray(_count_nonmasked(x, axis), dtype=mu.dtype, device=xp_device(x))
    statistic = n / 6 * (s**2 + k**2 / 4)

    chi2 = _SimpleChi2(xp.asarray(2., dtype=mu.dtype, device=xp_device(x)))
    pvalue = _get_pvalue(statistic, chi2, alternative='greater', symmetric=False, xp=xp)

    statistic = statistic[()] if statistic.ndim == 0 else statistic
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue

    return SignificanceResult(statistic, pvalue)

