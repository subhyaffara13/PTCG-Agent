import math


def expectile(a, alpha=0.5, *, weights=None, axis=None):
    r"""Compute the expectile at the specified level.

    Expectiles are a generalization of the expectation in the same way as
    quantiles are a generalization of the median. The expectile at level
    `alpha = 0.5` is the mean (average). See Notes for more details.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose expectile is desired.
    alpha : float, default: 0.5
        The level of the expectile; e.g., ``alpha=0.5`` gives the mean.
    weights : array_like, optional
        An array of weights associated with the values in `a`.
        The `weights` must be broadcastable to the same shape as `a`.
        Default is None, which gives each value a weight of 1.0.
        An integer valued weight element acts like repeating the corresponding
        observation in `a` that many times. See Notes for more details.
    axis : int or tuple of ints, default: None
        If an int or tuple of ints, the axis or axes of the input along which
        to compute the statistic. The statistic of each axis-slice (e.g. row)
        of the input will appear in a corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.

    Returns
    -------
    expectile : ndarray
        The empirical expectile at level `alpha`.

    See Also
    --------
    numpy.mean : Arithmetic average
    numpy.quantile : Quantile

    Notes
    -----
    In general, the expectile at level :math:`\alpha` of a random variable
    :math:`X` with cumulative distribution function (CDF) :math:`F` is given
    by the unique solution :math:`t` of:

    .. math::

        \alpha E((X - t)_+) = (1 - \alpha) E((t - X)_+) \,.

    Here, :math:`(x)_+ = \max(0, x)` is the positive part of :math:`x`.
    This equation can be equivalently written as:

    .. math::

        \alpha \int_t^\infty (x - t)\mathrm{d}F(x)
        = (1 - \alpha) \int_{-\infty}^t (t - x)\mathrm{d}F(x) \,.

    The empirical expectile at level :math:`\alpha` (`alpha`) of a sample
    :math:`a_i` (the array `a`) is defined by plugging in the empirical CDF of
    `a`. Given sample or case weights :math:`w` (the array `weights`), it
    reads :math:`F_a(x) = \frac{1}{\sum_i w_i} \sum_i w_i 1_{a_i \leq x}`
    with indicator function :math:`1_{A}`. This leads to the definition of the
    empirical expectile at level `alpha` as the unique solution :math:`t` of:

    .. math::

        \alpha \sum_{i=1}^n w_i (a_i - t)_+ =
            (1 - \alpha) \sum_{i=1}^n w_i (t - a_i)_+ \,.

    For :math:`\alpha=0.5`, this simplifies to the weighted average.
    Furthermore, the larger :math:`\alpha`, the larger the value of the
    expectile.

    As a final remark, the expectile at level :math:`\alpha` can also be
    written as a minimization problem. One often used choice is

    .. math::

        \operatorname{argmin}_t
        E(\lvert 1_{t\geq X} - \alpha\rvert(t - X)^2) \,.

    References
    ----------
    .. [1] W. K. Newey and J. L. Powell (1987), "Asymmetric Least Squares
           Estimation and Testing," Econometrica, 55, 819-847.
    .. [2] T. Gneiting (2009). "Making and Evaluating Point Forecasts,"
           Journal of the American Statistical Association, 106, 746 - 762.
           :doi:`10.48550/arXiv.0912.0902`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import expectile
    >>> a = [1, 4, 2, -1]
    >>> expectile(a, alpha=0.5) == np.mean(a)
    True
    >>> expectile(a, alpha=0.2)
    0.42857142857142855
    >>> expectile(a, alpha=0.8)
    2.5714285714285716
    >>> weights = [1, 3, 1, 1]
    >>> expectile(a, alpha=0.8, weights=weights)
    3.3333333333333335
    """
    xp = array_namespace(a, weights)
    a, weights = xp_promote(a, weights, force_floating=True, xp=xp)

    if alpha < 0 or alpha > 1:
        raise ValueError(
            "The expectile level alpha must be in the range [0, 1]."
        )

    if a.shape[-1] == 0:  #  Only for *testing* _axis_nan_policy decorator
        return _get_nan(a, xp=xp)

    # for simplicity, ensure that shape is (batch size, sample size) and at least 2d
    shape = a.shape  # remember original shape, though, to ensure correct output shape
    # `reshape` can't infer shape element -1 when array is size 0, so take `prod`
    a = xp.reshape(a, (math.prod(shape[:-1]), shape[-1]))
    weights = weights if weights is None else xp.reshape(weights, (-1, shape[-1]))

    # This is the empirical equivalent of Eq. (13) with identification
    # function from Table 9 (omitting a factor of 2) in [2] (their y is our
    # data a, their x is our t)
    def first_order(t, i):
        ai = a[i, ...].T
        wi = weights if weights is None else weights[i, ...].T
        return _xp_mean(xp.abs(xp.astype(ai <= t, ai.dtype) - alpha) * (t - ai),
                        weights=wi, axis=0)

    # axis is -1 per the decorator. Use mean to produce NaNs of the correct shape/type.
    x0 = xp.min(a, axis=-1)
    x1 = xp.max(a, axis=-1)

    # Note that the expectile is the unique solution, so no worries about
    # finding a wrong root.
    i = xp.arange(a.shape[0])
    res = find_root(first_order, (x0, x1), args=(i,))
    res = xp.reshape(res.x, shape[:-1])
    return res[()] if res.ndim == 0 else res

