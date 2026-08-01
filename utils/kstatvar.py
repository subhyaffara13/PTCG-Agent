
def kstatvar(data, n=2, *, axis=None):
    r"""Return an unbiased estimator of the variance of the k-statistic.

    See `kstat` and [1]_ for more details about the k-statistic.

    Parameters
    ----------
    data : array_like
        Input array.
    n : int, {1, 2}, optional
        Default is equal to 2.
    axis : int or None, default: None
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear
        in a corresponding element of the output. If ``None``, the input will
        be raveled before computing the statistic.

    Returns
    -------
    kstatvar : float
        The `n` th k-statistic variance.

    See Also
    --------
    kstat : Returns the n-th k-statistic.
    moment : Returns the n-th central moment about the mean for a sample.

    Notes
    -----
    Unbiased estimators of the variances of the first two k-statistics are given by

    .. math::

        \mathrm{var}(k_1) &= \frac{k_2}{n}, \\
        \mathrm{var}(k_2) &= \frac{2k_2^2n + (n-1)k_4}{n(n + 1)}.

    References
    ----------
    .. [1] http://mathworld.wolfram.com/k-Statistic.html

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng(92366746)

    As the sample size increases, the estimated variance of the k-statistic converges
    to zero.

    >>> for n in np.astype(np.logspace(1, 6, 6), int):
    ...     x = rng.normal(size=n)
    ...     kvar = stats.kstatvar(x, 1)
    ...     print(f"{n=:<8}: {kvar=:.3g}")
    n=10      : kvar=0.0954
    n=100     : kvar=0.00974
    n=1000    : kvar=0.000962
    n=10000   : kvar=0.0001
    n=100000  : kvar=9.94e-06
    n=1000000 : kvar=9.99e-07
    """  # noqa: E501
    xp = array_namespace(data)
    data = xp.asarray(data)
    if axis is None:
        data = xp.reshape(data, (-1,))
        axis = 0
    N = _count_nonmasked(data, axis, xp=xp)

    if n == 1:
        return kstat(data, n=2, axis=axis, _no_deco=True) * 1.0/N
    elif n == 2:
        k2 = kstat(data, n=2, axis=axis, _no_deco=True)
        k4 = kstat(data, n=4, axis=axis, _no_deco=True)
        return (2*N*k2**2 + (N-1)*k4) / (N*(N+1))
    else:
        raise ValueError("Only n=1 or n=2 supported.")

