
def hermeweight(x):
    """Weight function of the Hermite_e polynomials.

    The weight function is :math:`\\exp(-x^2/2)` and the interval of
    integration is :math:`[-\\inf, \\inf]`. the HermiteE polynomials are
    orthogonal, but not normalized, with respect to this weight function.

    Parameters
    ----------
    x : array_like
       Values at which the weight function will be computed.

    Returns
    -------
    w : ndarray
       The weight function at `x`.
    """
    w = np.exp(-.5 * x**2)
    return w

