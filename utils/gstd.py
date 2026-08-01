
def gstd(a, axis=0, ddof=1, *, keepdims=False, nan_policy='propagate'):
    r"""
    Calculate the geometric standard deviation of an array.

    The geometric standard deviation describes the spread of a set of numbers
    where the geometric mean is preferred. It is a multiplicative factor, and
    so a dimensionless quantity.

    It is defined as the exponential of the standard deviation of the
    natural logarithms of the observations.

    Parameters
    ----------
    a : array_like
        An array containing finite, strictly positive, real numbers.
    axis : int, tuple or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.
    ddof : int, optional
        Degree of freedom correction in the calculation of the
        geometric standard deviation. Default is 1.
    keepdims : bool, optional
        If this is set to ``True``, the axes which are reduced are left
        in the result as dimensions with length one. With this option,
        the result will broadcast correctly against the input array.
    nan_policy : {'propagate', 'omit', 'raise'}, default: 'propagate'
        Defines how to handle input NaNs.

        - ``propagate``: if a NaN is present in the axis slice (e.g. row) along
          which the statistic is computed, the corresponding entry of the output
          will be NaN.
        - ``omit``: NaNs will be omitted when performing the calculation.
          If insufficient data remains in the axis slice along which the
          statistic is computed, the corresponding entry of the output will be
          NaN.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    Returns
    -------
    gstd : ndarray or float
        An array of the geometric standard deviation. If `axis` is None or `a`
        is a 1d array a float is returned.

    See Also
    --------
    gmean : Geometric mean
    numpy.std : Standard deviation
    gzscore : Geometric standard score

    Notes
    -----
    Mathematically, the sample geometric standard deviation :math:`s_G` can be
    defined in terms of the natural logarithms of the observations
    :math:`y_i = \log(x_i)`:

    .. math::

        s_G = \exp(s), \quad s = \sqrt{\frac{1}{n - d} \sum_{i=1}^n (y_i - \bar y)^2}

    where :math:`n` is the number of observations, :math:`d` is the adjustment `ddof`
    to the degrees of freedom, and :math:`\bar y` denotes the mean of the natural
    logarithms of the observations. Note that the default ``ddof=1`` is different from
    the default value used by similar functions, such as `numpy.std` and `numpy.var`.

    When an observation is infinite, the geometric standard deviation is
    NaN (undefined). Non-positive observations will also produce NaNs in the
    output because the *natural* logarithm (as opposed to the *complex*
    logarithm) is defined and finite only for positive reals.
    The geometric standard deviation is sometimes confused with the exponential
    of the standard deviation, ``exp(std(a))``. Instead, the geometric standard
    deviation is ``exp(std(log(a)))``.

    References
    ----------
    .. [1] "Geometric standard deviation", *Wikipedia*,
           https://en.wikipedia.org/wiki/Geometric_standard_deviation.
    .. [2] Kirkwood, T. B., "Geometric means and measures of dispersion",
           Biometrics, vol. 35, pp. 908-909, 1979

    Examples
    --------
    Find the geometric standard deviation of a log-normally distributed sample.
    Note that the standard deviation of the distribution is one; on a
    log scale this evaluates to approximately ``exp(1)``.

    >>> import numpy as np
    >>> from scipy.stats import gstd
    >>> rng = np.random.default_rng()
    >>> sample = rng.lognormal(mean=0, sigma=1, size=1000)
    >>> gstd(sample)
    2.810010162475324

    Compute the geometric standard deviation of a multidimensional array and
    of a given axis.

    >>> a = np.arange(1, 25).reshape(2, 3, 4)
    >>> gstd(a, axis=None)
    2.2944076136018947
    >>> gstd(a, axis=2)
    array([[1.82424757, 1.22436866, 1.13183117],
           [1.09348306, 1.07244798, 1.05914985]])
    >>> gstd(a, axis=(1,2))
    array([2.12939215, 1.22120169])

    """
    xp = array_namespace(a)
    a = xp_promote(a, force_floating=True, xp=xp)

    kwargs = dict(axis=axis, correction=ddof, keepdims=keepdims, nan_policy=nan_policy)
    with np.errstate(invalid='ignore', divide='ignore'):
        res = xp.exp(_xp_var(xp.log(a), **kwargs)**0.5)

    if not is_lazy_array(a) and xp.any(a <= 0):
        message = ("The geometric standard deviation is only defined if all elements "
                   "are greater than or equal to zero; otherwise, the result is NaN.")
        warnings.warn(message, RuntimeWarning, stacklevel=2)

    return res


def gstd(*args, **kwargs):
    kwargs.pop('_no_deco', None)
    return stats.gstd(*args, **kwargs)

