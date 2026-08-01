
def lagweight(x):
    """Weight function of the Laguerre polynomials.

    The weight function is :math:`exp(-x)` and the interval of integration
    is :math:`[0, \\inf]`. The Laguerre polynomials are orthogonal, but not
    normalized, with respect to this weight function.

    Parameters
    ----------
    x : array_like
       Values at which the weight function will be computed.

    Returns
    -------
    w : ndarray
       The weight function at `x`.

    Examples
    --------
    >>> from numpy.polynomial.laguerre import lagweight
    >>> x = np.array([0, 1, 2])
    >>> lagweight(x)
    array([1.        , 0.36787944, 0.13533528])

    """
    w = np.exp(-x)
    return w

