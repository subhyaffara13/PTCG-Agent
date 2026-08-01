
def zscore(a, axis=0, ddof=0, nan_policy='propagate'):
    """
    Compute the z score.

    Compute the z score of each value in the sample, relative to the
    sample mean and standard deviation.

    Parameters
    ----------
    a : array_like
        An array like object containing the sample data.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.
    ddof : int, optional
        Degrees of freedom correction in the calculation of the
        standard deviation. Default is 0.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.  Note that when the value is 'omit',
        nans in the input also propagate to the output, but they do not affect
        the z-scores computed for the non-nan values.

    Returns
    -------
    zscore : array_like
        The z-scores, standardized by mean and standard deviation of
        input array `a`.

    See Also
    --------
    numpy.mean : Arithmetic average
    numpy.std : Arithmetic standard deviation
    scipy.stats.gzscore : Geometric standard score

    Notes
    -----
    This function preserves ndarray subclasses, and works also with
    matrices and masked arrays (it uses `asanyarray` instead of
    `asarray` for parameters).

    References
    ----------
    .. [1] "Standard score", *Wikipedia*,
           https://en.wikipedia.org/wiki/Standard_score.
    .. [2] Huck, S. W., Cross, T. L., Clark, S. B, "Overcoming misconceptions
           about Z-scores", Teaching Statistics, vol. 8, pp. 38-40, 1986

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([ 0.7972,  0.0767,  0.4383,  0.7866,  0.8091,
    ...                0.1954,  0.6307,  0.6599,  0.1065,  0.0508])
    >>> from scipy import stats
    >>> stats.zscore(a)
    array([ 1.1273, -1.247 , -0.0552,  1.0923,  1.1664, -0.8559,  0.5786,
            0.6748, -1.1488, -1.3324])

    Computing along a specified axis, using n-1 degrees of freedom
    (``ddof=1``) to calculate the standard deviation:

    >>> b = np.array([[ 0.3148,  0.0478,  0.6243,  0.4608],
    ...               [ 0.7149,  0.0775,  0.6072,  0.9656],
    ...               [ 0.6341,  0.1403,  0.9759,  0.4064],
    ...               [ 0.5918,  0.6948,  0.904 ,  0.3721],
    ...               [ 0.0921,  0.2481,  0.1188,  0.1366]])
    >>> stats.zscore(b, axis=1, ddof=1)
    array([[-0.19264823, -1.28415119,  1.07259584,  0.40420358],
           [ 0.33048416, -1.37380874,  0.04251374,  1.00081084],
           [ 0.26796377, -1.12598418,  1.23283094, -0.37481053],
           [-0.22095197,  0.24468594,  1.19042819, -1.21416216],
           [-0.82780366,  1.4457416 , -0.43867764, -0.1792603 ]])

    An example with ``nan_policy='omit'``:

    >>> x = np.array([[25.11, 30.10, np.nan, 32.02, 43.15],
    ...               [14.95, 16.06, 121.25, 94.35, 29.81]])
    >>> stats.zscore(x, axis=1, nan_policy='omit')
    array([[-1.13490897, -0.37830299,         nan, -0.08718406,  1.60039602],
           [-0.91611681, -0.89090508,  1.4983032 ,  0.88731639, -0.5785977 ]])
    """
    return zmap(a, a, axis=axis, ddof=ddof, nan_policy=nan_policy)

