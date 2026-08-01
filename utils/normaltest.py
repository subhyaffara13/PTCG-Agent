
def normaltest(a, axis=0):
    """
    Tests whether a sample differs from a normal distribution.

    Parameters
    ----------
    a : array_like
        The array containing the data to be tested.
    axis : int or None, optional
        Axis along which to compute test. Default is 0. If None,
        compute over the whole array `a`.

    Returns
    -------
    statistic : float or array
        ``s^2 + k^2``, where ``s`` is the z-score returned by `skewtest` and
        ``k`` is the z-score returned by `kurtosistest`.
    pvalue : float or array
         A 2-sided chi squared probability for the hypothesis test.

    Notes
    -----
    For more details about `normaltest`, see `scipy.stats.normaltest`.

    """
    a, axis = _chk_asarray(a, axis)
    s, _ = skewtest(a, axis)
    k, _ = kurtosistest(a, axis)
    k2 = s*s + k*k

    return NormaltestResult(k2, distributions.chi2.sf(k2, 2))


def normaltest(a, axis=0, nan_policy='propagate'):
    r"""Test whether a sample differs from a normal distribution.

    This function tests the null hypothesis that a sample comes
    from a normal distribution.  It is based on D'Agostino and
    Pearson's [1]_, [2]_ test that combines skew and kurtosis to
    produce an omnibus test of normality.

    Parameters
    ----------
    a : array_like
        The array containing the sample to be tested. Must contain
        at least eight observations.
    axis : int or None, optional
        Axis along which to compute test. Default is 0. If None,
        compute over the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    Returns
    -------
    statistic : float or array
        ``s^2 + k^2``, where ``s`` is the z-score returned by `skewtest` and
        ``k`` is the z-score returned by `kurtosistest`.
    pvalue : float or array
        A 2-sided chi squared probability for the hypothesis test.

    See Also
    --------
    :ref:`hypothesis_normaltest` : Extended example

    References
    ----------
    .. [1] D'Agostino, R. B. (1971), "An omnibus test of normality for
            moderate and large sample size", Biometrika, 58, 341-348
    .. [2] D'Agostino, R. and Pearson, E. S. (1973), "Tests for departure from
            normality", Biometrika, 60, 613-622

    Examples
    --------

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> pts = 1000
    >>> a = rng.normal(0, 1, size=pts)
    >>> b = rng.normal(2, 1, size=pts)
    >>> x = np.concatenate((a, b))
    >>> res = stats.normaltest(x)
    >>> res.statistic
    53.619...  # random
    >>> res.pvalue
    2.273917413209226e-12  # random

    For a more detailed example, see :ref:`hypothesis_normaltest`.
    """
    xp = array_namespace(a)

    s, _ = skewtest(a, axis, _no_deco=True)
    k, _ = kurtosistest(a, axis, _no_deco=True)
    statistic = s*s + k*k

    chi2 = _SimpleChi2(xp.asarray(2., dtype=statistic.dtype, device=xp_device(a)))
    pvalue = _get_pvalue(statistic, chi2, alternative='greater', symmetric=False, xp=xp)

    statistic = statistic[()] if statistic.ndim == 0 else statistic
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue

    return NormaltestResult(statistic, pvalue)

