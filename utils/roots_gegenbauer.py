
def roots_gegenbauer(n, alpha, mu=False):
    r"""Gauss-Gegenbauer quadrature.

    Compute the sample points and weights for Gauss-Gegenbauer
    quadrature. The sample points are the roots of the nth degree
    Gegenbauer polynomial, :math:`C^{\alpha}_n(x)`. These sample
    points and weights correctly integrate polynomials of degree
    :math:`2n - 1` or less over the interval :math:`[-1, 1]` with
    weight function :math:`w(x) = (1 - x^2)^{\alpha - 1/2}`. See
    22.2.3 in [AS]_ for more details.

    Parameters
    ----------
    n : int
        quadrature order.
    alpha : float
        alpha must be > -0.5.
    mu : bool, optional
        If True, return the sum of the weights, optional.

    Returns
    -------
    x : ndarray
        Sample points
    w : ndarray
        Weights
    mu : float
        Sum of the weights

    See Also
    --------
    scipy.integrate.fixed_quad

    References
    ----------
    .. [AS] Milton Abramowitz and Irene A. Stegun, eds.
        Handbook of Mathematical Functions with Formulas,
        Graphs, and Mathematical Tables. New York: Dover, 1972.

    """
    m = int(n)
    if n < 1 or n != m:
        raise ValueError("n must be a positive integer.")
    if alpha < -0.5:
        raise ValueError("alpha must be greater than -0.5.")
    elif alpha == 0.0:
        # C(n,0,x) == 0 uniformly, however, as alpha->0, C(n,alpha,x)->T(n,x)
        # strictly, we should just error out here, since the roots are not
        # really defined, but we used to return something useful, so let's
        # keep doing so.
        return roots_chebyt(n, mu)

    if alpha <= 170:
        mu0 = (np.sqrt(np.pi) * _ufuncs.gamma(alpha + 0.5)) \
              / _ufuncs.gamma(alpha + 1)
    else:
        # For large alpha we use a Taylor series expansion around inf,
        # expressed as a 6th order polynomial of a^-1 and using Horner's
        # method to minimize computation and maximize precision
        inv_alpha = 1. / alpha
        coeffs = np.array([0.000207186, -0.00152206, -0.000640869,
                           0.00488281, 0.0078125, -0.125, 1.])
        mu0 = coeffs[0]
        for term in range(1, len(coeffs)):
            mu0 = mu0 * inv_alpha + coeffs[term]
        mu0 = mu0 * np.sqrt(np.pi / alpha)
    def an_func(k):
        return 0.0 * k
    def bn_func(k):
        return np.sqrt(k * (k + 2 * alpha - 1) / (4 * (k + alpha) * (k + alpha - 1)))
    def f(n, x):
        return _ufuncs.eval_gegenbauer(n, alpha, x)
    def df(n, x):
        return (
            -n * x * _ufuncs.eval_gegenbauer(n, alpha, x)
            + (n + 2 * alpha - 1) * _ufuncs.eval_gegenbauer(n - 1, alpha, x)
        ) / (1 - x ** 2)
    return _gen_roots_and_weights(m, mu0, an_func, bn_func, f, df, True, mu)

