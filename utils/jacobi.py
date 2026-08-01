
def jacobi(x, y):
    """Jacobi symbol (x / y)."""
    if y <= 0 or not y % 2:
        raise ValueError("y should be an odd positive integer")
    x %= y
    if not x:
        return int(y == 1)
    if y == 1 or x == 1:
        return 1
    if gcd(x, y) != 1:
        return 0
    j = 1
    while x != 0:
        while x % 2 == 0 and x > 0:
            x >>= 1
            if y % 8 in [3, 5]:
                j = -j
        x, y = y, x
        if x % 4 == y % 4 == 3:
            j = -j
        x %= y
    return j


def jacobi(n, alpha, beta, monic=False):
    r"""Jacobi polynomial.

    Defined to be the solution of

    .. math::

        \begin{aligned}
        (1 - x^2)\frac{d^2}{dx^2} P_n^{(\alpha, \beta)}(x)
        &+ \left(\beta - \alpha - (\alpha + \beta + 2)x\right)
        \frac{d}{dx} P_n^{(\alpha, \beta)}(x) \\
        &+ n(n + \alpha + \beta + 1) P_n^{(\alpha, \beta)}(x) = 0
        \end{aligned}

    for :math:`\alpha, \beta > -1`; :math:`P_n^{(\alpha, \beta)}` is a
    polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    alpha : float
        Parameter, must be greater than -1.
    beta : float
        Parameter, must be greater than -1.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    P : orthopoly1d
        Jacobi polynomial.

    Notes
    -----
    For fixed :math:`\alpha, \beta`, the polynomials
    :math:`P_n^{(\alpha, \beta)}` are orthogonal over :math:`[-1, 1]`
    with weight function :math:`(1 - x)^\alpha(1 + x)^\beta`.

    References
    ----------
    .. [AS] Milton Abramowitz and Irene A. Stegun, eds.
        Handbook of Mathematical Functions with Formulas,
        Graphs, and Mathematical Tables. New York: Dover, 1972.

    Examples
    --------
    The Jacobi polynomials satisfy the recurrence relation:

    .. math::
        P_n^{(\alpha, \beta-1)}(x) - P_n^{(\alpha-1, \beta)}(x)
          = P_{n-1}^{(\alpha, \beta)}(x)

    This can be verified, for example, for :math:`\alpha = \beta = 2`
    and :math:`n = 1` over the interval :math:`[-1, 1]`:

    >>> import numpy as np
    >>> from scipy.special import jacobi
    >>> x = np.arange(-1.0, 1.0, 0.01)
    >>> np.allclose(jacobi(0, 2, 2)(x),
    ...             jacobi(1, 2, 1)(x) - jacobi(1, 1, 2)(x))
    True

    Plot of the Jacobi polynomial :math:`P_5^{(\alpha, -0.5)}` for
    different values of :math:`\alpha`:

    >>> import matplotlib.pyplot as plt
    >>> x = np.arange(-1.0, 1.0, 0.01)
    >>> fig, ax = plt.subplots()
    >>> ax.set_ylim(-2.0, 2.0)
    >>> ax.set_title(r'Jacobi polynomials $P_5^{(\alpha, -0.5)}$')
    >>> for alpha in np.arange(0, 4, 1):
    ...     ax.plot(x, jacobi(5, alpha, -0.5)(x), label=rf'$\alpha={alpha}$')
    >>> plt.legend(loc='best')
    >>> plt.show()

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    def wfunc(x):
        return (1 - x) ** alpha * (1 + x) ** beta
    if n == 0:
        return orthopoly1d([], [], 1.0, 1.0, wfunc, (-1, 1), monic,
                           eval_func=np.ones_like)
    x, w, mu = roots_jacobi(n, alpha, beta, mu=True)
    ab1 = alpha + beta + 1.0
    hn = 2**ab1 / (2 * n + ab1) * _gam(n + alpha + 1)
    hn *= _gam(n + beta + 1.0) / _gam(n + 1) / _gam(n + ab1)
    kn = _gam(2 * n + ab1) / 2.0**n / _gam(n + 1) / _gam(n + ab1)
    # here kn = coefficient on x^n term
    p = orthopoly1d(x, w, hn, kn, wfunc, (-1, 1), monic,
                    lambda x: _ufuncs.eval_jacobi(n, alpha, beta, x))
    return p


def jacobi(ctx, n, a, b, x, **kwargs):
    if not ctx.isnpint(a):
        def h(n):
            return (([], [], [a+n+1], [n+1, a+1], [-n, a+b+n+1], [a+1], (1-x)*0.5),)
        return ctx.hypercomb(h, [n], **kwargs)
    if not ctx.isint(b):
        def h(n, a):
            return (([], [], [-b], [n+1, -b-n], [-n, a+b+n+1], [b+1], (x+1)*0.5),)
        return ctx.hypercomb(h, [n, a], **kwargs)
    # XXX: determine appropriate limit
    return ctx.binomial(n+a,n) * ctx.hyp2f1(-n,1+n+a+b,a+1,(1-x)/2, **kwargs)

