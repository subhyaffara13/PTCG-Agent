
def correlation(X, Y, condition=None, **kwargs):
    r"""
    Correlation of two random expressions, also known as correlation
    coefficient or Pearson's correlation.

    Explanation
    ===========

    The normalized expectation that the two variables will rise
    and fall together

    .. math::
        correlation(X,Y) = E((X-E(X))(Y-E(Y)) / (\sigma_x  \sigma_y))

    Examples
    ========

    >>> from sympy.stats import Exponential, correlation
    >>> from sympy import Symbol

    >>> rate = Symbol('lambda', positive=True, real=True)
    >>> X = Exponential('X', rate)
    >>> Y = Exponential('Y', rate)

    >>> correlation(X, X)
    1
    >>> correlation(X, Y)
    0
    >>> correlation(X, Y + rate*X)
    1/sqrt(1 + lambda**(-2))
    """
    return covariance(X, Y, condition, **kwargs)/(std(X, condition, **kwargs)
     * std(Y, condition, **kwargs))


def correlation(u, v, w=None, centered=True):
    """
    Compute the correlation distance between two 1-D arrays.

    The correlation distance between `u` and `v`, is
    defined as

    .. math::

        1 - \\frac{(u - \\bar{u}) \\cdot (v - \\bar{v})}
                  {{\\|(u - \\bar{u})\\|}_2 {\\|(v - \\bar{v})\\|}_2}

    where :math:`\\bar{u}` is the mean of the elements of `u`
    and :math:`x \\cdot y` is the dot product of :math:`x` and :math:`y`.

    Parameters
    ----------
    u : (N,) array_like of floats
        Input array.
    v : (N,) array_like of floats
        Input array.
    w : (N,) array_like of floats, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0
    centered : bool, optional
        If True, `u` and `v` will be centered. Default is True.

    Returns
    -------
    correlation : double
        The correlation distance between 1-D array `u` and `v`.

    Examples
    --------
    Find the correlation between two arrays.

    >>> from scipy.spatial.distance import correlation
    >>> correlation([1, 0, 1], [1, 1, 0])
    1.5

    Using a weighting array, the correlation can be calculated as:

    >>> correlation([1, 0, 1], [1, 1, 0], w=[0.9, 0.1, 0.1])
    1.1

    If centering is not needed, the correlation can be calculated as:

    >>> correlation([1, 0, 1], [1, 1, 0], centered=False)
    0.5
    """
    u = _validate_vector(u)
    v = _validate_vector(v)
    if np.iscomplexobj(u) or np.iscomplexobj(v):
        msg = "`u` and `v` must be real."
        raise TypeError(msg)
    if w is not None:
        w = _validate_weights(w)
        w = w / w.sum()
    if centered:
        if w is not None:
            umu = np.dot(u, w)
            vmu = np.dot(v, w)
        else:
            umu = np.mean(u)
            vmu = np.mean(v)
        u = u - umu
        v = v - vmu
    if w is not None:
        vw = v * w
        uw = u * w
    else:
        vw, uw = v, u
    uv = np.dot(u, vw)
    uu = np.dot(u, uw)
    vv = np.dot(v, vw)
    dist = 1.0 - uv / math.sqrt(uu * vv)
    # Clip the result to avoid rounding error
    return np.clip(dist, 0.0, 2.0)

