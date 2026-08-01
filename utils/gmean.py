
def gmean(a, axis=0, dtype=None, weights=None):
    r"""Compute the weighted geometric mean along the specified axis.

    The weighted geometric mean of the array :math:`a_i` associated to weights
    :math:`w_i` is:

    .. math::

        \exp \left( \frac{ \sum_{i=1}^n w_i \ln a_i }{ \sum_{i=1}^n w_i }
                   \right) \, ,

    and, with equal weights, it gives:

    .. math::

        \sqrt[n]{ \prod_{i=1}^n a_i } \, .

    Parameters
    ----------
    a : array_like
        Input array or object that can be converted to an array.
    axis : int or None, optional
        Axis along which the geometric mean is computed. Default is 0.
        If None, compute over the whole array `a`.
    dtype : dtype, optional
        (Floating point) dtype to which numerical arguments are cast before performing
        the calculation. If `dtype` is not specified, it defaults to the floating point
        result dtype of the numerical arguments.
    weights : array_like, optional
        The `weights` array must be broadcastable to the same shape as `a`.
        Default is None, which gives each value a weight of 1.0.

    Returns
    -------
    gmean : ndarray
        See `dtype` parameter above.

    See Also
    --------
    numpy.mean : Arithmetic average
    numpy.average : Weighted average
    hmean : Harmonic mean

    Notes
    -----
    The sample geometric mean is the exponential of the mean of the natural
    logarithms of the observations.
    Negative observations will produce NaNs in the output because the *natural*
    logarithm (as opposed to the *complex* logarithm) is defined only for
    non-negative reals.

    References
    ----------
    .. [1] "Weighted Geometric Mean", *Wikipedia*,
           https://en.wikipedia.org/wiki/Weighted_geometric_mean.
    .. [2] Grossman, J., Grossman, M., Katz, R., "Averages: A New Approach",
           Archimedes Foundation, 1983

    Examples
    --------
    >>> from scipy.stats import gmean
    >>> gmean([1, 4])
    2.0
    >>> gmean([1, 2, 3, 4, 5, 6, 7])
    3.3800151591412964
    >>> gmean([1, 4, 7], weights=[3, 1, 3])
    2.80668351922014

    """
    xp = array_namespace(a, weights)
    dtype = (xp_result_type(a, weights, force_floating=True, xp=xp)
             if dtype is None else dtype)
    a = xp.asarray(a, dtype=dtype)

    if weights is not None:
        weights = xp.asarray(weights, dtype=dtype)

    with np.errstate(divide='ignore'):
        log_a = xp.log(a)

    return xp.exp(_xp_mean(log_a, axis=axis, weights=weights))

