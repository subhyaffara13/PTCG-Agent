
def iqr(x, axis=None, rng=(25, 75), scale=1.0, nan_policy='propagate',
        interpolation='linear', keepdims=False):
    r"""
    Compute the interquartile range of the data along the specified axis.

    The interquartile range (IQR) is the difference between the 75th and
    25th percentile of the data. It is a measure of the dispersion
    similar to standard deviation or variance, but is much more robust
    against outliers [2]_.

    The ``rng`` parameter allows this function to compute other
    percentile ranges than the actual IQR. For example, setting
    ``rng=(0, 100)`` is equivalent to `numpy.ptp`.

    The IQR of an empty array is `np.nan`.

    .. versionadded:: 0.18.0

    Parameters
    ----------
    x : array_like
        Input array or object that can be converted to an array.
    axis : int or sequence of int, optional
        Axis along which the range is computed. The default is to
        compute the IQR for the entire array.
    rng : Two-element sequence containing floats in range of [0,100] optional
        Percentiles over which to compute the range. Each must be
        between 0 and 100, inclusive. The default is the true IQR:
        ``(25, 75)``. The order of the elements is not important.
    scale : scalar or str or array_like of reals, optional
        The numerical value of scale will be divided out of the final
        result. The following string value is also recognized:

        * 'normal' : Scale by
          :math:`2 \sqrt{2} erf^{-1}(\frac{1}{2}) \approx 1.349`.

        The default is 1.0.
        Array-like `scale` of real dtype is also allowed, as long
        as it broadcasts correctly to the output such that
        ``out / scale`` is a valid operation. The output dimensions
        depend on the input array, `x`, the `axis` argument, and the
        `keepdims` flag.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    interpolation : str, optional

        Specifies the interpolation method to use when the percentile
        boundaries lie between two data points ``i`` and ``j``.
        The following options are available (default is 'linear'):

        * 'linear': ``i + (j - i)*fraction``, where ``fraction`` is the
          fractional part of the index surrounded by ``i`` and ``j``.
        * 'lower': ``i``.
        * 'higher': ``j``.
        * 'nearest': ``i`` or ``j`` whichever is nearest.
        * 'midpoint': ``(i + j)/2``.

        For NumPy >= 1.22.0, the additional options provided by the ``method``
        keyword of `numpy.percentile` are also valid.

    keepdims : bool, optional
        If this is set to True, the reduced axes are left in the
        result as dimensions with size one. With this option, the result
        will broadcast correctly against the original array `x`.

    Returns
    -------
    iqr : scalar or ndarray
        If ``axis=None``, a scalar is returned. If the input contains
        integers or floats of smaller precision than ``np.float64``, then the
        output data-type is ``np.float64``. Otherwise, the output data-type is
        the same as that of the input.

    See Also
    --------
    numpy.std, numpy.var

    References
    ----------
    .. [1] "Interquartile range" https://en.wikipedia.org/wiki/Interquartile_range
    .. [2] "Robust measures of scale" https://en.wikipedia.org/wiki/Robust_measures_of_scale
    .. [3] "Quantile" https://en.wikipedia.org/wiki/Quantile

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import iqr
    >>> x = np.array([[10, 7, 4], [3, 2, 1]])
    >>> x
    array([[10,  7,  4],
           [ 3,  2,  1]])
    >>> iqr(x)
    4.0
    >>> iqr(x, axis=0)
    array([ 3.5,  2.5,  1.5])
    >>> iqr(x, axis=1)
    array([ 3.,  1.])
    >>> iqr(x, axis=1, keepdims=True)
    array([[ 3.],
           [ 1.]])

    """
    xp = array_namespace(x)

    # An error may be raised here, so fail-fast, before doing lengthy
    # computations, even though `scale` is not used until later
    if isinstance(scale, str):
        scale_key = scale.lower()
        if scale_key not in _scale_conversions:
            raise ValueError(f"{scale} not a valid scale for `iqr`")
        scale = _scale_conversions[scale_key]

    if len(rng) != 2:
        raise TypeError("`rng` must be a two element sequence.")

    if np.isnan(rng).any():  # OK to use NumPy; this shouldn't be an array
        raise ValueError("`rng` must not contain NaNs.")

    rng = (rng[0]/100, rng[1]/100) if rng[0] < rng[1] else (rng[1]/100, rng[0]/100)

    if rng[0] < 0 or rng[1] > 1:
        raise ValueError("Elements of `rng` must be in the range [0, 100].")

    if interpolation in {'lower', 'midpoint', 'higher', 'nearest'}:
        interpolation = '_' + interpolation

    rng = xp.asarray(rng, dtype=xp_result_type(x, force_floating=True, xp=xp))
    pct = stats.quantile(x, rng, axis=-1, method=interpolation, keepdims=True)
    out = pct[..., 1:2] - pct[..., 0:1]

    if scale != 1.0:
        out /= scale

    out = out if keepdims else xp.squeeze(out, axis=-1)
    return out[()] if out.ndim == 0 else out

