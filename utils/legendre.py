
def legendre(x, y):
    """Legendre symbol (x / y).

    Following the implementation of gmpy2,
    the error is raised only when y is an even number.
    """
    if y <= 0 or not y % 2:
        raise ValueError("y should be an odd prime")
    x %= y
    if not x:
        return 0
    if pow(x, (y - 1) // 2, y) == 1:
        return 1
    return -1


def legendre(n, monic=False):
    r"""Legendre polynomial.

    Defined to be the solution of

    .. math::
        \frac{d}{dx}\left[(1 - x^2)\frac{d}{dx}P_n(x)\right]
          + n(n + 1)P_n(x) = 0;

    :math:`P_n(x)` is a polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    P : orthopoly1d
        Legendre polynomial.

    Notes
    -----
    The polynomials :math:`P_n` are orthogonal over :math:`[-1, 1]`
    with weight function 1.

    Examples
    --------
    Generate the 3rd-order Legendre polynomial 1/2*(5x^3 + 0x^2 - 3x + 0):

    >>> from scipy.special import legendre
    >>> legendre(3)
    poly1d([ 2.5,  0. , -1.5,  0. ])

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w = roots_legendre(n1)
    if n == 0:
        x, w = [], []
    hn = 2.0 / (2 * n + 1)
    kn = _gam(2 * n + 1) / _gam(n + 1)**2 / 2.0**n
    p = orthopoly1d(x, w, hn, kn, wfunc=lambda x: 1.0, limits=(-1, 1),
                    monic=monic,
                    eval_func=lambda x: _ufuncs.eval_legendre(n, x))
    return p


def legendre(ctx, n, x, **kwargs):
    if ctx.isint(n):
        n = int(n)
        # Accuracy near zeros
        if (n + (n < 0)) & 1:
            if not x:
                return x
            mag = ctx.mag(x)
            if mag < -2*ctx.prec-10:
                return x
            if mag < -5:
                ctx.prec += -mag
    return ctx.hyp2f1(-n,n+1,1,(1-x)/2, **kwargs)

