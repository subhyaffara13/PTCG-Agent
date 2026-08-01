
def Hermite(name, a1, a2):
    r"""
    Create a discrete random variable with a Hermite distribution.

    Explanation
    ===========

    The density of the Hermite distribution is given by

    .. math::
        f(x):= e^{-a_1 -a_2}\sum_{j=0}^{\left \lfloor x/2 \right \rfloor}
                    \frac{a_{1}^{x-2j}a_{2}^{j}}{(x-2j)!j!}

    Parameters
    ==========

    a1 : A Positive number greater than equal to 0.
    a2 : A Positive number greater than equal to 0.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Hermite, density, E, variance
    >>> from sympy import Symbol

    >>> a1 = Symbol("a1", positive=True)
    >>> a2 = Symbol("a2", positive=True)
    >>> x = Symbol("x")

    >>> H = Hermite("H", a1=5, a2=4)

    >>> density(H)(2)
    33*exp(-9)/2

    >>> E(H)
    13

    >>> variance(H)
    21

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Hermite_distribution

    """

    return rv(name, HermiteDistribution, a1, a2)


def hermite(n, monic=False):
    r"""Physicist's Hermite polynomial.

    Defined by

    .. math::

        H_n(x) = (-1)^ne^{x^2}\frac{d^n}{dx^n}e^{-x^2};

    :math:`H_n` is a polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    H : orthopoly1d
        Physicist's Hermite polynomial.

    Notes
    -----
    The polynomials :math:`H_n` are orthogonal over :math:`(-\infty,
    \infty)` with weight function :math:`e^{-x^2}`.

    Examples
    --------
    >>> from scipy import special
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    >>> p_monic = special.hermite(3, monic=True)
    >>> p_monic
    poly1d([ 1. ,  0. , -1.5,  0. ])
    >>> p_monic(1)
    -0.49999999999999983
    >>> x = np.linspace(-3, 3, 400)
    >>> y = p_monic(x)
    >>> plt.plot(x, y)
    >>> plt.title("Monic Hermite polynomial of degree 3")
    >>> plt.xlabel("x")
    >>> plt.ylabel("H_3(x)")
    >>> plt.show()

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w = roots_hermite(n1)
    def wfunc(x):
        return exp(-x * x)
    if n == 0:
        x, w = [], []
    hn = 2**n * _gam(n + 1) * sqrt(pi)
    kn = 2**n
    p = orthopoly1d(x, w, hn, kn, wfunc, (-inf, inf), monic,
                    lambda x: _ufuncs.eval_hermite(n, x))
    return p


def hermite(ctx, n, z, **kwargs):
    return ctx.hypercomb(lambda: _hermite_param(ctx, n, z, 0), [], **kwargs)

