
def roots_sh_chebyt(n, mu=False):
    r"""Gauss-Chebyshev (first kind, shifted) quadrature.

    Compute the sample points and weights for Gauss-Chebyshev
    quadrature. The sample points are the roots of the nth degree
    shifted Chebyshev polynomial of the first kind, :math:`T_n(x)`.
    These sample points and weights correctly integrate polynomials of
    degree :math:`2n - 1` or less over the interval :math:`[0, 1]`
    with weight function :math:`w(x) = 1/\sqrt{x - x^2}`. See 22.2.8
    in [AS]_ for more details.

    Parameters
    ----------
    n : int
        quadrature order.
    mu : bool, optional
        If True, return the sum of the weights, optional.

    Returns
    -------
    x : ndarray
        Sample points.
    w : ndarray
        Weights.
    mu : float
        Sum of the weights.

    See Also
    --------
    scipy.integrate.fixed_quad

    References
    ----------
    .. [AS] Milton Abramowitz and Irene A. Stegun, eds.
        Handbook of Mathematical Functions with Formulas,
        Graphs, and Mathematical Tables. New York: Dover, 1972.

    """
    xw = roots_chebyt(n, mu)
    return ((xw[0] + 1) / 2,) + xw[1:]

