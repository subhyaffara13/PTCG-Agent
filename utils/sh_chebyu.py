
def sh_chebyu(n, monic=False):
    r"""Shifted Chebyshev polynomial of the second kind.

    Defined as :math:`U^*_n(x) = U_n(2x - 1)` for :math:`U_n` the nth
    Chebyshev polynomial of the second kind.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    U : orthopoly1d
        Shifted Chebyshev polynomial of the second kind.

    Notes
    -----
    The polynomials :math:`U^*_n` are orthogonal over :math:`[0, 1]`
    with weight function :math:`(x - x^2)^{1/2}`.

    Examples
    --------
    Evaluate the shifted Chebyshev polynomial of the second kind :math:`U^*_3` at
    :math:`x = 0.75`:

    >>> import numpy as np
    >>> from scipy.special import chebyu, sh_chebyu
    >>> np.isclose(sh_chebyu(3)(0.75), -1.0)
    True

    The polynomial :math:`U^*_n` is the Chebyshev polynomial
    :math:`U_n` shifted from :math:`[-1, 1]` to :math:`[0, 1]`:

    >>> x = np.linspace(0, 1, 5)
    >>> np.allclose(sh_chebyu(3)(x), chebyu(3)(2*x - 1))
    True

    Plot :math:`U^*_n` for several values of :math:`n`:

    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(0, 1, 400)
    >>> fig, ax = plt.subplots()
    >>> for n in range(4):
    ...     ax.plot(x, sh_chebyu(n)(x), label=rf"$U^*_{n}$")
    >>> ax.set_title(r"Shifted Chebyshev polynomials $U^*_n$")
    >>> ax.set_xlabel("x")
    >>> ax.legend(loc="best")
    >>> plt.show()

    """
    base = sh_jacobi(n, 2.0, 1.5, monic=monic)
    if monic:
        return base
    factor = 4**n
    base._scale(factor)
    return base

