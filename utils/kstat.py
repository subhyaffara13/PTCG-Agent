
def kstat(data, n=2, *, axis=None):
    r"""
    Return the `n` th k-statistic ( ``1<=n<=4`` so far).

    The `n` th k-statistic ``k_n`` is the unique symmetric unbiased estimator of the
    `n` th cumulant :math:`\kappa_n` [1]_ [2]_.

    Parameters
    ----------
    data : array_like
        Input array.
    n : int, {1, 2, 3, 4}, optional
        Default is equal to 2.
    axis : int or None, default: None
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear
        in a corresponding element of the output. If ``None``, the input will
        be raveled before computing the statistic.

    Returns
    -------
    kstat : float
        The `n` th k-statistic.

    See Also
    --------
    kstatvar : Returns an unbiased estimator of the variance of the k-statistic
    moment : Returns the n-th central moment about the mean for a sample.

    Notes
    -----
    For a sample size :math:`n`, the first few k-statistics are given by

    .. math::

        k_1 &= \frac{S_1}{n}, \\
        k_2 &= \frac{nS_2 - S_1^2}{n(n-1)}, \\
        k_3 &= \frac{2S_1^3 - 3nS_1S_2 + n^2S_3}{n(n-1)(n-2)}, \\
        k_4 &= \frac{-6S_1^4 + 12nS_1^2S_2 - 3n(n-1)S_2^2 - 4n(n+1)S_1S_3
        + n^2(n+1)S_4}{n (n-1)(n-2)(n-3)},

    where

    .. math::

        S_r \equiv \sum_{i=1}^n X_i^r,

    and :math:`X_i` is the :math:`i` th data point.

    References
    ----------
    .. [1] http://mathworld.wolfram.com/k-Statistic.html

    .. [2] http://mathworld.wolfram.com/Cumulant.html

    Examples
    --------
    >>> from scipy import stats
    >>> from numpy.random import default_rng
    >>> rng = default_rng()

    As sample size increases, `n`-th moment and `n`-th k-statistic converge to the
    same number (although they aren't identical). In the case of the normal
    distribution, they converge to zero.

    >>> for i in range(2,8):
    ...     x = rng.normal(size=10**i)
    ...     m, k = stats.moment(x, 3), stats.kstat(x, 3)
    ...     print(f"{i=}: {m=:.3g}, {k=:.3g}, {(m-k)=:.3g}")
    i=2: m=-0.631, k=-0.651, (m-k)=0.0194  # random
    i=3: m=0.0282, k=0.0283, (m-k)=-8.49e-05
    i=4: m=-0.0454, k=-0.0454, (m-k)=1.36e-05
    i=6: m=7.53e-05, k=7.53e-05, (m-k)=-2.26e-09
    i=7: m=0.00166, k=0.00166, (m-k)=-4.99e-09
    i=8: m=-2.88e-06 k=-2.88e-06, (m-k)=8.63e-13
    """
    xp = array_namespace(data)
    data = xp.asarray(data)
    if n > 4 or n < 1:
        raise ValueError("k-statistics only supported for 1<=n<=4")
    n = int(n)
    if axis is None:
        data = xp.reshape(data, (-1,))
        axis = 0

    N = _count_nonmasked(data, axis, xp=xp)

    S = [None] + [xp.sum(data**k, axis=axis) for k in range(1, n + 1)]
    if n == 1:
        return S[1] * 1.0/N
    elif n == 2:
        return (N*S[2] - S[1]**2.0) / (N*(N - 1.0))
    elif n == 3:
        return (2*S[1]**3 - 3*N*S[1]*S[2] + N*N*S[3]) / (N*(N - 1.0)*(N - 2.0))
    elif n == 4:
        return ((-6*S[1]**4 + 12*N*S[1]**2 * S[2] - 3*N*(N-1.0)*S[2]**2 -
                 4*N*(N+1)*S[1]*S[3] + N*N*(N+1)*S[4]) /
                (N*(N-1.0)*(N-2.0)*(N-3.0)))
    else:
        raise ValueError("Should not be here.")

