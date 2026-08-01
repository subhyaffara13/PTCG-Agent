
def pcfd(ctx, n, z, **kwargs):
    r"""
    Gives the parabolic cylinder function in Whittaker's notation
    `D_n(z) = U(-n-1/2, z)` (see :func:`~mpmath.pcfu`).
    It solves the differential equation

    .. math ::

        y'' + \left(n + \frac{1}{2} - \frac{1}{4} z^2\right) y = 0.

    and can be represented in terms of Hermite polynomials
    (see :func:`~mpmath.hermite`) as

    .. math ::

        D_n(z) = 2^{-n/2} e^{-z^2/4} H_n\left(\frac{z}{\sqrt{2}}\right).

    **Plots**

    .. literalinclude :: /plots/pcfd.py
    .. image :: /plots/pcfd.png

    **Examples**

        >>> from mpmath import *
        >>> mp.dps = 25; mp.pretty = True
        >>> pcfd(0,0); pcfd(1,0); pcfd(2,0); pcfd(3,0)
        1.0
        0.0
        -1.0
        0.0
        >>> pcfd(4,0); pcfd(-3,0)
        3.0
        0.6266570686577501256039413
        >>> pcfd('1/2', 2+3j)
        (-5.363331161232920734849056 - 3.858877821790010714163487j)
        >>> pcfd(2, -10)
        1.374906442631438038871515e-9

    Verifying the differential equation::

        >>> n = mpf(2.5)
        >>> y = lambda z: pcfd(n,z)
        >>> z = 1.75
        >>> chop(diff(y,z,2) + (n+0.5-0.25*z**2)*y(z))
        0.0

    Rational Taylor series expansion when `n` is an integer::

        >>> taylor(lambda z: pcfd(5,z), 0, 7)
        [0.0, 15.0, 0.0, -13.75, 0.0, 3.96875, 0.0, -0.6015625]

    """
    return ctx.hypercomb(lambda: _hermite_param(ctx, n, z, 1), [], **kwargs)

