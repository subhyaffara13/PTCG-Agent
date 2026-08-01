
def sh_chebyt(n, monic=False):
    r"""Shifted Chebyshev polynomial of the first kind.

    Defined as :math:`T^*_n(x) = T_n(2x - 1)` for :math:`T_n` the nth
    Chebyshev polynomial of the first kind.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    T : orthopoly1d
        Shifted Chebyshev polynomial of the first kind.

    Notes
    -----
    The polynomials :math:`T^*_n` are orthogonal over :math:`[0, 1]`
    with weight function :math:`(x - x^2)^{-1/2}`.

    Examples
    --------
    Evaluate the shifted Chebyshev polynomial of the first kind :math:`T^*_3` at
    :math:`x = 0.75`:

    >>> import numpy as np
    >>> from scipy.special import chebyt, sh_chebyt
    >>> np.isclose(sh_chebyt(3)(0.75), -1.0)
    True

    The polynomial :math:`T^*_n` is the Chebyshev polynomial
    :math:`T_n` shifted from :math:`[-1, 1]` to :math:`[0, 1]`:

    >>> x = np.linspace(0, 1, 5)
    >>> np.allclose(sh_chebyt(3)(x), chebyt(3)(2*x - 1))
    True

    Plot :math:`T^*_n` for several values of :math:`n`:

    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(0, 1, 400)
    >>> fig, ax = plt.subplots()
    >>> for n in range(4):
    ...     ax.plot(x, sh_chebyt(n)(x), label=rf"$T^*_{n}$")
    >>> ax.set_title(r"Shifted Chebyshev polynomials $T^*_n$")
    >>> ax.set_xlabel("x")
    >>> ax.legend(loc="best")
    >>> plt.show()

    """
    base = sh_jacobi(n, 0.0, 0.5, monic=monic)
    if monic:
        return base
    if n > 0:
        factor = 4**n / 2.0
    else:
        factor = 1.0
    base._scale(factor)
    return base

