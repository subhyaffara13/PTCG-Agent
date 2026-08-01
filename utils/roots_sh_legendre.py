
def roots_sh_legendre(n, mu=False):
    r"""Gauss-Legendre (shifted) quadrature.

    Compute the sample points and weights for Gauss-Legendre
    quadrature. The sample points are the roots of the nth degree
    shifted Legendre polynomial :math:`P^*_n(x)`. These sample points
    and weights correctly integrate polynomials of degree :math:`2n -
    1` or less over the interval :math:`[0, 1]` with weight function
    :math:`w(x) = 1.0`. See 2.2.11 in [AS]_ for details.

    Parameters
    ----------
    n : int
        quadrature order
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

    Examples
    --------

    Compute nodes and weights for a 7th-order shifted Gauss-Legendre quadrature:

    >>> from scipy.special import roots_sh_legendre, eval_sh_legendre
    >>> x, w = roots_sh_legendre(7)
    >>> x
    array([0.02544604, 0.12923441, 0.29707742, 0.5, 0.70292258, 0.87076559,
        0.97455396])
    >>> w
    array([0.06474248, 0.1398527, 0.19091503, 0.20897959, 0.19091503, 0.1398527,
        0.06474248])

    Verify that ``x`` are the roots of the degree-7 shifted Legendre polynomial:

    >>> eval_sh_legendre(7, x)
    array([5.55111512e-16, 1.11022302e-16,  3.33066907e-16,  0.00000000e+00,
        -2.22044605e-16, -1.11022302e-16, -1.85962357e-15])

    The sum of the weights for shifted Gauss-Legendre quadrature is always 1:

    >>> x, w, mu = roots_sh_legendre(10, mu=True)
    >>> mu 
    1.0  # Sum of weights of shifted Gauss-Legendre quadrature is always 1

    """
    x, w = roots_legendre(n)
    x = (x + 1) / 2
    w /= 2
    if mu:
        return x, w, 1.0
    else:
        return x, w

