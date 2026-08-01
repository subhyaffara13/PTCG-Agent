
def brunnermunzel(x, y, alternative="two-sided", distribution="t"):
    """
    Compute the Brunner-Munzel test on samples x and y.

    Any missing values in `x` and/or `y` are discarded.

    The Brunner-Munzel test is a nonparametric test of the null hypothesis that
    when values are taken one by one from each group, the probabilities of
    getting large values in both groups are equal.
    Unlike the Wilcoxon-Mann-Whitney's U test, this does not require the
    assumption of equivariance of two groups. Note that this does not assume
    the distributions are same. This test works on two independent samples,
    which may have different sizes.

    Parameters
    ----------
    x, y : array_like
        Array of samples, should be one-dimensional.
    alternative : 'less', 'two-sided', or 'greater', optional
        Whether to get the p-value for the one-sided hypothesis ('less'
        or 'greater') or for the two-sided hypothesis ('two-sided').
        Defaults value is 'two-sided' .
    distribution : 't' or 'normal', optional
        Whether to get the p-value by t-distribution or by standard normal
        distribution.
        Defaults value is 't' .

    Returns
    -------
    statistic : float
        The Brunner-Munzer W statistic.
    pvalue : float
        p-value assuming a t distribution. One-sided or
        two-sided, depending on the choice of `alternative` and `distribution`.

    See Also
    --------
    mannwhitneyu : Mann-Whitney rank test on two samples.

    Notes
    -----
    For more details on `brunnermunzel`, see `scipy.stats.brunnermunzel`.

    Examples
    --------
    >>> from scipy.stats.mstats import brunnermunzel
    >>> import numpy as np
    >>> x1 = [1, 2, np.nan, np.nan, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1]
    >>> x2 = [3, 3, 4, 3, 1, 2, 3, 1, 1, 5, 4]
    >>> brunnermunzel(x1, x2)
    BrunnerMunzelResult(statistic=1.4723186918922935, pvalue=0.15479415300426624)  # may vary

    """  # noqa: E501
    x = ma.asarray(x).compressed().view(ndarray)
    y = ma.asarray(y).compressed().view(ndarray)
    nx = len(x)
    ny = len(y)
    if nx == 0 or ny == 0:
        return BrunnerMunzelResult(np.nan, np.nan)
    rankc = rankdata(np.concatenate((x,y)))
    rankcx = rankc[0:nx]
    rankcy = rankc[nx:nx+ny]
    rankcx_mean = np.mean(rankcx)
    rankcy_mean = np.mean(rankcy)
    rankx = rankdata(x)
    ranky = rankdata(y)
    rankx_mean = np.mean(rankx)
    ranky_mean = np.mean(ranky)

    Sx = np.sum(np.power(rankcx - rankx - rankcx_mean + rankx_mean, 2.0))
    Sx /= nx - 1
    Sy = np.sum(np.power(rankcy - ranky - rankcy_mean + ranky_mean, 2.0))
    Sy /= ny - 1

    wbfn = nx * ny * (rankcy_mean - rankcx_mean)
    wbfn /= (nx + ny) * np.sqrt(nx * Sx + ny * Sy)

    if distribution == "t":
        df_numer = np.power(nx * Sx + ny * Sy, 2.0)
        df_denom = np.power(nx * Sx, 2.0) / (nx - 1)
        df_denom += np.power(ny * Sy, 2.0) / (ny - 1)
        df = df_numer / df_denom
        p = distributions.t.cdf(wbfn, df)
    elif distribution == "normal":
        p = distributions.norm.cdf(wbfn)
    else:
        raise ValueError(
            "distribution should be 't' or 'normal'")

    if alternative == "greater":
        pass
    elif alternative == "less":
        p = 1 - p
    elif alternative == "two-sided":
        p = 2 * np.min([p, 1-p])
    else:
        raise ValueError(
            "alternative should be 'less', 'greater' or 'two-sided'")

    return BrunnerMunzelResult(wbfn, p)


def brunnermunzel(x, y, alternative="two-sided", distribution="t",
                  nan_policy='propagate', *, axis=0):
    """Compute the Brunner-Munzel test on samples x and y.

    The Brunner-Munzel test is a nonparametric test of the null hypothesis that
    when values are taken one by one from each group, the probabilities of
    getting large values in both groups are equal.
    Unlike the Wilcoxon-Mann-Whitney's U test, this does not require the
    assumption of equivariance of two groups. Note that this does not assume
    the distributions are same. This test works on two independent samples,
    which may have different sizes.

    Parameters
    ----------
    x, y : array_like
        Array of samples, should be one-dimensional.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.
        The following options are available (default is 'two-sided'):

        * 'two-sided'
        * 'less': one-sided
        * 'greater': one-sided

    distribution : {'t', 'normal'}, optional
        Defines how to get the p-value.
        The following options are available (default is 't'):

        * 't': get the p-value by t-distribution
        * 'normal': get the p-value by standard normal distribution.

    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    axis : int or None, default=0
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear
        in a corresponding element of the output. If None, the input will be
        raveled before computing the statistic.

    Returns
    -------
    statistic : float
        The Brunner-Munzer W statistic.
    pvalue : float
        p-value assuming an t distribution. One-sided or
        two-sided, depending on the choice of `alternative` and `distribution`.

    See Also
    --------
    mannwhitneyu : Mann-Whitney rank test on two samples.

    Notes
    -----
    Brunner and Munzel recommended to estimate the p-value by t-distribution
    when the size of data is 50 or less. If the size is lower than 10, it would
    be better to use permuted Brunner Munzel test (see [2]_).

    References
    ----------
    .. [1] Brunner, E. and Munzel, U. "The nonparametric Benhrens-Fisher
           problem: Asymptotic theory and a small-sample approximation".
           Biometrical Journal. Vol. 42(2000): 17-25.
    .. [2] Neubert, K. and Brunner, E. "A studentized permutation test for the
           non-parametric Behrens-Fisher problem". Computational Statistics and
           Data Analysis. Vol. 51(2007): 5192-5204.

    Examples
    --------
    >>> from scipy import stats
    >>> x1 = [1,2,1,1,1,1,1,1,1,1,2,4,1,1]
    >>> x2 = [3,3,4,3,1,2,3,1,1,5,4]
    >>> w, p_value = stats.brunnermunzel(x1, x2)
    >>> w
    3.1374674823029505
    >>> p_value
    0.0057862086661515377

    """
    # _axis_nan_policy decorator ensures we can work along the last axis
    xp = array_namespace(x, y)
    length_x = x.shape[-1]
    nx = _count_nonmasked(x, axis=-1)
    ny = _count_nonmasked(y, axis=-1)

    rankc = rankdata(xp.concat((x, y), axis=axis), axis=-1)
    rankcx = rankc[..., :length_x]
    rankcy = rankc[..., length_x:]
    rankcx_mean = xp.mean(rankcx, axis=-1, keepdims=True)
    rankcy_mean = xp.mean(rankcy, axis=-1, keepdims=True)
    rankx = rankdata(x, axis=-1)
    ranky = rankdata(y, axis=-1)
    rankx_mean = xp.mean(rankx, axis=-1, keepdims=True)
    ranky_mean = xp.mean(ranky, axis=-1, keepdims=True)

    temp_x = rankcx - rankx - rankcx_mean + rankx_mean
    Sx = xp.vecdot(temp_x, temp_x, axis=-1)
    Sx /= nx - 1
    temp_y = rankcy - ranky - rankcy_mean + ranky_mean
    Sy = xp.vecdot(temp_y, temp_y, axis=-1)
    Sy /= ny - 1

    rankcx_mean = xp.squeeze(rankcx_mean, axis=-1)
    rankcy_mean = xp.squeeze(rankcy_mean, axis=-1)
    wbfn = nx * ny * (rankcy_mean - rankcx_mean)
    wbfn /= (nx + ny) * xp.sqrt(nx * Sx + ny * Sy)

    if distribution == "t":
        df_numer = xp.pow(nx * Sx + ny * Sy, 2.0)
        df_denom = xp.pow(nx * Sx, 2.0) / (nx - 1)
        df_denom += xp.pow(ny * Sy, 2.0) / (ny - 1)
        df = df_numer / df_denom

        if not is_lazy_array(df_numer) and not is_lazy_array(df_denom) and (
                xp.any(df_numer == 0) and xp.any(df_denom == 0)):
            message = ("p-value cannot be estimated with `distribution='t' "
                       "because degrees of freedom parameter is undefined "
                       "(0/0). Try using `distribution='normal'")
            warnings.warn(message, RuntimeWarning, stacklevel=2)

        distribution = _SimpleStudentT(df)
    elif distribution == "normal":
        distribution = _SimpleNormal()
    else:
        raise ValueError(
            "distribution should be 't' or 'normal'")

    p = _get_pvalue(-wbfn, distribution, alternative, xp=xp)

    return BrunnerMunzelResult(wbfn, p)

