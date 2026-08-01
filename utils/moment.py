
def moment(X, n, c=0, condition=None, *, evaluate=True, **kwargs):
    """
    Return the nth moment of a random expression about c.

    .. math::
        moment(X, c, n) = E((X-c)^{n})

    Default value of c is 0.

    Examples
    ========

    >>> from sympy.stats import Die, moment, E
    >>> X = Die('X', 6)
    >>> moment(X, 1, 6)
    -5/2
    >>> moment(X, 2)
    91/6
    >>> moment(X, 1) == E(X)
    True
    """
    from sympy.stats.symbolic_probability import Moment
    if evaluate:
        return Moment(X, n, c, condition).doit()
    return Moment(X, n, c, condition).rewrite(Integral)


def moment(a, moment=1, axis=0):
    """
    Calculates the nth moment about the mean for a sample.

    Parameters
    ----------
    a : array_like
       data
    moment : int, optional
       order of central moment that is returned
    axis : int or None, optional
       Axis along which the central moment is computed. Default is 0.
       If None, compute over the whole array `a`.

    Returns
    -------
    n-th central moment : ndarray or float
       The appropriate moment along the given axis or over all values if axis
       is None. The denominator for the moment calculation is the number of
       observations, no degrees of freedom correction is done.

    Notes
    -----
    For more details about `moment`, see `scipy.stats.moment`.

    """
    a, axis = _chk_asarray(a, axis)
    if a.size == 0:
        moment_shape = list(a.shape)
        del moment_shape[axis]
        dtype = a.dtype.type if a.dtype.kind in 'fc' else np.float64
        # empty array, return nan(s) with shape matching `moment`
        out_shape = (moment_shape if np.isscalar(moment)
                     else [len(moment)] + moment_shape)
        if len(out_shape) == 0:
            return dtype(np.nan)
        else:
            return ma.array(np.full(out_shape, np.nan, dtype=dtype))

    # for array_like moment input, return a value for each.
    if not np.isscalar(moment):
        mean = a.mean(axis, keepdims=True)
        mmnt = [_moment(a, i, axis, mean=mean) for i in moment]
        return ma.array(mmnt)
    else:
        return _moment(a, moment, axis)


def moment(a, order=1, axis=0, nan_policy='propagate', *, center=None):
    r"""Calculate the nth moment about the mean for a sample.

    A moment is a specific quantitative measure of the shape of a set of
    points. It is often used to calculate coefficients of skewness and kurtosis
    due to its close relationship with them.

    Parameters
    ----------
    a : array_like
       Input array.
    order : int or 1-D array_like of ints, optional
       Order of central moment that is returned. Default is 1.
    axis : int or None, optional
       Axis along which the central moment is computed. Default is 0.
       If None, compute over the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    center : float or None, optional
       The point about which moments are taken. This can be the sample mean,
       the origin, or any other be point. If `None` (default) compute the
       center as the sample mean.

    Returns
    -------
    n-th moment about the `center` : ndarray or float
       The appropriate moment along the given axis or over all values if axis
       is None. The denominator for the moment calculation is the number of
       observations, no degrees of freedom correction is done.

    See Also
    --------
    kurtosis, skew, describe

    Notes
    -----
    The k-th moment of a data sample is:

    .. math::

        m_k = \frac{1}{n} \sum_{i = 1}^n (x_i - c)^k

    Where `n` is the number of samples, and `c` is the center around which the
    moment is calculated. This function uses exponentiation by squares [1]_ for
    efficiency.

    Note that, if `a` is an empty array (``a.size == 0``), array `moment` with
    one element (`moment.size == 1`) is treated the same as scalar `moment`
    (``np.isscalar(moment)``). This might produce arrays of unexpected shape.

    References
    ----------
    .. [1] https://eli.thegreenplace.net/2009/03/21/efficient-integer-exponentiation-algorithms

    Examples
    --------
    >>> from scipy.stats import moment
    >>> moment([1, 2, 3, 4, 5], order=1)
    0.0
    >>> moment([1, 2, 3, 4, 5], order=2)
    2.0

    """
    xp = array_namespace(a)
    a, center, order = xp_promote(a, center, order, force_floating=True, xp=xp)

    if not is_lazy_array(order) and xp.any(order != xp.round(order)):
        raise ValueError("All elements of `order` must be integral.")

    # _axis_nan_policy decorator ensures that axis=-1
    if order.ndim > 0:
        order = xp.reshape(order, (-1,) + (1,)*a.ndim)
        return _moment(a, order, axis=-1, center=center)
    else:
        res = _moment(a, order, axis=-1, center=center)
        return res[()] if res.ndim == 0 else res

