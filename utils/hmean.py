
def hmean(a, axis=0, dtype=None, *, weights=None):
    r"""Calculate the weighted harmonic mean along the specified axis.

    The weighted harmonic mean of the array :math:`a_i` associated to weights
    :math:`w_i` is:

    .. math::

        \frac{ \sum_{i=1}^n w_i }{ \sum_{i=1}^n \frac{w_i}{a_i} } \, ,

    and, with equal weights, it gives:

    .. math::

        \frac{ n }{ \sum_{i=1}^n \frac{1}{a_i} } \, .

    Parameters
    ----------
    a : array_like
        Input array, masked array or object that can be converted to an array.
    axis : int or None, optional
        Axis along which the harmonic mean is computed. Default is 0.
        If None, compute over the whole array `a`.
    dtype : dtype, optional
        (Floating point) dtype to which numerical arguments are cast before performing
        the calculation. If `dtype` is not specified, it defaults to the floating point
        result dtype of the numerical arguments.
    weights : array_like, optional
        The weights array can either be 1-D (in which case its length must be
        the size of `a` along the given `axis`) or of the same shape as `a`.
        Default is None, which gives each value a weight of 1.0.

        .. versionadded:: 1.9

    Returns
    -------
    hmean : ndarray
        See `dtype` parameter above.

    See Also
    --------
    numpy.mean : Arithmetic average
    numpy.average : Weighted average
    gmean : Geometric mean

    Notes
    -----
    The sample harmonic mean is the reciprocal of the mean of the reciprocals
    of the observations.

    The harmonic mean is computed over a single dimension of the input
    array, axis=0 by default, or all values in the array if axis=None.
    float64 intermediate and return values are used for integer inputs.

    The harmonic mean is only defined if all observations are non-negative;
    otherwise, the result is NaN.

    References
    ----------
    .. [1] "Weighted Harmonic Mean", *Wikipedia*,
           https://en.wikipedia.org/wiki/Harmonic_mean#Weighted_harmonic_mean
    .. [2] Ferger, F., "The nature and use of the harmonic mean", Journal of
           the American Statistical Association, vol. 26, pp. 36-40, 1931

    Examples
    --------
    >>> from scipy.stats import hmean
    >>> hmean([1, 4])
    1.6000000000000001
    >>> hmean([1, 2, 3, 4, 5, 6, 7])
    2.6997245179063363
    >>> hmean([1, 4, 7], weights=[3, 1, 3])
    1.9029126213592233

    """
    xp = array_namespace(a, weights)
    dtype = (xp_result_type(a, weights, force_floating=True, xp=xp)
             if dtype is None else dtype)
    a = xp.asarray(a, dtype=dtype)

    if weights is not None:
        weights = xp.asarray(weights, dtype=dtype)

    negative_mask = a < 0
    a = xp.where(negative_mask, xp.nan, a)

    if not is_lazy_array(negative_mask) and xp.any(negative_mask):
        message = ("The harmonic mean is only defined if all elements are "
                   "non-negative; otherwise, the result is NaN.")
        warnings.warn(message, RuntimeWarning, stacklevel=2)

    with np.errstate(divide='ignore'):
        return 1.0 / _xp_mean(1.0 / a, axis=axis, weights=weights)

