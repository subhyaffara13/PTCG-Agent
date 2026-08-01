
def hermitenorm(n, monic=False):
    r"""Probabilist's Hermite polynomial.

    Defined by

    .. math::

        He_n(x) = (-1)^ne^{x^2/2}\frac{d^n}{dx^n}e^{-x^2/2};

    :math:`He_n` is a polynomial of degree :math:`n`.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    He : orthopoly1d
        Probabilist's Hermite polynomial.

    Notes
    -----

    The polynomials :math:`He_n` are orthogonal over :math:`(-\infty,
    \infty)` with weight function :math:`e^{-x^2/2}`.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.special import hermitenorm

    >>> p_monic = hermitenorm(3)
    >>> p_monic
    poly1d([ 1.,  0., -3.,  0.])

    Evaluate the probabilist's Hermite polynomial of degree 3 at x = 1:

    >>> p_monic(1)
    np.float64(-2.0)

    Plot probabilist's Hermite polynomials of degree 0 to 4:
    
    >>> x = np.linspace(-3, 3, 100)
    >>> fig, ax = plt.subplots()
    >>> for i in range(5):
    ...     ax.plot(x, hermitenorm(i)(x), label=f"n={i}")
    >>> plt.title(f"Probabilist's Hermite polynomials $He_n$")
    >>> plt.xlabel("x")
    >>> plt.ylabel(rf"$He_n(x)$")
    >>> plt.legend(loc="best")
    >>> plt.show()

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w = roots_hermitenorm(n1)
    def wfunc(x):
        return exp(-x * x / 2.0)
    if n == 0:
        x, w = [], []
    hn = sqrt(2 * pi) * _gam(n + 1)
    kn = 1.0
    p = orthopoly1d(x, w, hn, kn, wfunc=wfunc, limits=(-inf, inf), monic=monic,
                    eval_func=lambda x: _ufuncs.eval_hermitenorm(n, x))
    return p

