
def sh_legendre(n, monic=False):
    r"""
    Shifted Legendre polynomial.

    Defined as :math:`P^*_n(x) = P_n(2x - 1)` for :math:`P_n` the nth
    Legendre polynomial.

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
        Shifted Legendre polynomial.

    See Also
    --------
    scipy.special.legendre
    scipy.special.roots_sh_legendre

    Notes
    -----
    The polynomials :math:`P^*_n` are orthogonal over :math:`[0, 1]`
    with weight function 1.

    Examples
    --------
    The shifted Legendre polynomials :math:`P_n^*` are related
    to the non-shifted polynomials :math:`P_n` by
    :math:`P_n^*(x) = P_n(2x - 1)`. We can verify this on the
    interval :math:`[0, 1]`:

    >>> import numpy as np
    >>> from scipy.special import sh_legendre, legendre
    >>> from scipy.integrate import trapezoid
    >>> x = np.arange(0.0, 1.0, 0.01)
    >>> n = 3
    >>> np.allclose(sh_legendre(n)(x), legendre(n)(2*x - 1))
    True

    The polynomials :math:`P_n^*` satisfy a recurrence
    relation obtained by the change of variables
    :math:`t = 2x - 1` in the standard Legendre recurrence:

    .. math::

        (n+1) P_{n+1}^*(x) = (2n+1)(2x-1)\,P_n^*(x) - n\,P_{n-1}^*(x).

    This can be easily checked on :math:`[0, 1]`
    for :math:`n = 3`:

    >>> n = 3
    >>> x = np.linspace(0.0, 1.0, 101)
    >>> lhs = (n + 1) * sh_legendre(n + 1)(x)
    >>> rhs = (
    ...     (2*n + 1) * (2*x - 1) * sh_legendre(n)(x)
    ...     - n * sh_legendre(n - 1)(x)
    ... )
    >>> np.allclose(lhs, rhs)
    True

    Orthogonality over :math:`[0,1]` with weight 1 can be
    checked numerically; for example, :math:`P_2^*`
    is orthogonal to :math:`P_3^*`:

    >>> x = np.linspace(0.0, 1.0, 400)
    >>> y = sh_legendre(2)(x) * sh_legendre(3)(x)
    >>> np.isclose(trapezoid(y, x), 0.0, atol=1e-12)
    True
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    def wfunc(x):
        return 0.0 * x + 1.0
    if n == 0:
        return orthopoly1d([], [], 1.0, 1.0, wfunc, (0, 1), monic,
                           lambda x: _ufuncs.eval_sh_legendre(n, x))
    x, w = roots_sh_legendre(n)
    hn = 1.0 / (2 * n + 1.0)
    kn = _gam(2 * n + 1) / _gam(n + 1)**2
    p = orthopoly1d(x, w, hn, kn, wfunc, limits=(0, 1), monic=monic,
                    eval_func=lambda x: _ufuncs.eval_sh_legendre(n, x))
    return p

