
def hermweight(x):
    """
    Weight function of the Hermite polynomials.

    The weight function is :math:`\\exp(-x^2)` and the interval of
    integration is :math:`[-\\inf, \\inf]`. the Hermite polynomials are
    orthogonal, but not normalized, with respect to this weight function.

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
    >>> import numpy as np
    >>> from numpy.polynomial.hermite import hermweight
    >>> x = np.arange(-2, 2)
    >>> hermweight(x)
    array([0.01831564, 0.36787944, 1.        , 0.36787944])

    """
    w = np.exp(-x**2)
    return w

