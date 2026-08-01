
def gegenbauer(n, alpha, monic=False):
    r"""Gegenbauer (ultraspherical) polynomial.

    Defined to be the solution of the second-order linear ordinary differential equation

    .. math::
        (1 - x^2)\frac{d^2}{dx^2}C_n^{(\alpha)}(x)
          - (2\alpha + 1)x\frac{d}{dx}C_n^{(\alpha)}(x)
          + n(n + 2\alpha)C_n^{(\alpha)}(x) = 0

    for :math:`\alpha > -1/2`; :math:`C_n^{(\alpha)}` is a polynomial
    of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    alpha : float
        Parameter, must be greater than -0.5.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    C : orthopoly1d
        Gegenbauer polynomial.

    Notes
    -----
    The polynomials :math:`C_n^{(\alpha)}` are orthogonal on
    :math:`[-1,1]` with respect to the weight function :math:`(1 - x^2)^{(\alpha -
    1/2)}`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import special
    >>> import matplotlib.pyplot as plt

    We can initialize a variable ``p`` as a Gegenbauer polynomial using the
    `gegenbauer` function and evaluate at a point ``x = 1``.

    >>> p = special.gegenbauer(3, 0.5, monic=False)
    >>> p
    poly1d([ 2.5,  0. , -1.5,  0. ])
    >>> p(1)
    1.0

    To evaluate ``p`` at various points ``x`` in the interval ``(-3, 3)``,
    simply pass an array ``x`` to ``p`` as follows:

    >>> x = np.linspace(-3, 3, 400)
    >>> y = p(x)

    We can then visualize ``x, y`` using `matplotlib.pyplot`.

    >>> fig, ax = plt.subplots()
    >>> ax.plot(x, y)
    >>> ax.set_title("Gegenbauer (ultraspherical) polynomial of degree 3")
    >>> ax.set_xlabel("x")
    >>> ax.set_ylabel(r"$C_3^{(0.5)}(x)$")
    >>> plt.show()

    """
    if not np.isfinite(alpha) or alpha <= -0.5 :
        raise ValueError("`alpha` must be a finite number greater than -1/2")
    base = jacobi(n, alpha - 0.5, alpha - 0.5, monic=monic)
    if monic or n == 0:
        return base
    #  Abrahmowitz and Stegan 22.5.20
    factor = (_gam(2*alpha + n) * _gam(alpha + 0.5) /
              _gam(2*alpha) / _gam(alpha + 0.5 + n))
    base._scale(factor)
    base.__dict__['_eval_func'] = lambda x: _ufuncs.eval_gegenbauer(float(n),
                                                                    alpha, x)
    return base


def gegenbauer(ctx, n, a, z, **kwargs):
    # Special cases: a+0.5, a*2 poles
    if ctx.isnpint(a):
        return 0*(z+n)
    if ctx.isnpint(a+0.5):
        # TODO: something else is required here
        # E.g.: gegenbauer(-2, -0.5, 3) == -12
        if ctx.isnpint(n+1):
            raise NotImplementedError("Gegenbauer function with two limits")
        def h(a):
            a2 = 2*a
            T = [], [], [n+a2], [n+1, a2], [-n, n+a2], [a+0.5], 0.5*(1-z)
            return [T]
        return ctx.hypercomb(h, [a], **kwargs)
    def h(n):
        a2 = 2*a
        T = [], [], [n+a2], [n+1, a2], [-n, n+a2], [a+0.5], 0.5*(1-z)
        return [T]
    return ctx.hypercomb(h, [n], **kwargs)

