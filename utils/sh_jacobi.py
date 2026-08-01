
def sh_jacobi(n, p, q, monic=False):
    r"""Shifted Jacobi polynomial.

    Defined by

    .. math::

        G_n^{(p, q)}(x)
          = \binom{2n + p - 1}{n}^{-1}P_n^{(p - q, q - 1)}(2x - 1),

    where :math:`P_n^{(\cdot, \cdot)}` is the nth Jacobi polynomial.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    p : float
        Parameter, must have :math:`p > q - 1`.
    q : float
        Parameter, must be greater than 0.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    G : orthopoly1d
        Shifted Jacobi polynomial.

    Notes
    -----
    For fixed :math:`p, q`, the polynomials :math:`G_n^{(p, q)}` are
    orthogonal over :math:`[0, 1]` with weight function :math:`(1 -
    x)^{p - q}x^{q - 1}`.

    Examples
    --------
    Evaluate the shifted Jacobi polynomial :math:`G_3^{(2, 1)}` at
    :math:`x = 0.5`:

    >>> import numpy as np
    >>> from scipy.special import binom, jacobi, sh_jacobi
    >>> np.isclose(sh_jacobi(3, 2, 1)(0.5), -3/280)
    True

    The polynomial is related to the Jacobi polynomial
    :math:`P_n^{(p - q, q - 1)}`:

    >>> x = np.linspace(0, 1, 5)
    >>> n, p, q = 3, 2, 1
    >>> scale = 1 / binom(2*n + p - 1, n)
    >>> np.allclose(sh_jacobi(n, p, q)(x),
    ...             scale * jacobi(n, p - q, q - 1)(2*x - 1))
    True

    Plot :math:`G_3^{(p, 1)}` for several values of :math:`p`:

    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(0, 1, 400)
    >>> fig, ax = plt.subplots()
    >>> for p in [1, 2, 3]:
    ...     ax.plot(x, sh_jacobi(3, p, 1)(x), label=rf"$p={p}$")
    >>> ax.set_title(r"Shifted Jacobi polynomials $G_3^{(p, 1)}$")
    >>> ax.set_xlabel("x")
    >>> ax.legend(loc="best")
    >>> plt.show()

    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    def wfunc(x):
        return (1.0 - x) ** (p - q) * x ** (q - 1.0)
    if n == 0:
        return orthopoly1d([], [], 1.0, 1.0, wfunc, (-1, 1), monic,
                           eval_func=np.ones_like)
    n1 = n
    x, w = roots_sh_jacobi(n1, p, q)
    hn = _gam(n + 1) * _gam(n + q) * _gam(n + p) * _gam(n + p - q + 1)
    hn /= (2 * n + p) * (_gam(2 * n + p)**2)
    # kn = 1.0 in standard form so monic is redundant. Kept for compatibility.
    kn = 1.0
    pp = orthopoly1d(x, w, hn, kn, wfunc=wfunc, limits=(0, 1), monic=monic,
                     eval_func=lambda x: _ufuncs.eval_sh_jacobi(n, p, q, x))
    return pp

