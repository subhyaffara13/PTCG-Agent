
def chebys(n, monic=False):
    r"""Chebyshev polynomial of the second kind on :math:`[-2, 2]`.

    Defined as :math:`S_n(x) = U_n(x/2)` where :math:`U_n` is the
    nth Chebyshev polynomial of the second kind.

    Parameters
    ----------
    n : int
        Degree of the polynomial.
    monic : bool, optional
        If `True`, scale the leading coefficient to be 1. Default is
        `False`.

    Returns
    -------
    S : orthopoly1d
        Chebyshev polynomial of the second kind on :math:`[-2, 2]`.

    See Also
    --------
    chebyu : Chebyshev polynomial of the second kind

    Notes
    -----
    The polynomials :math:`S_n(x)` are orthogonal over :math:`[-2, 2]`
    with weight function :math:`\sqrt{1 - (x/2)^2}`.

    References
    ----------
    .. [1] Abramowitz and Stegun, "Handbook of Mathematical Functions"
           Section 22. National Bureau of Standards, 1972.

    Examples
    --------
    Evaluate the Chebyshev polynomial of the second kind :math:`S_3` at :math:`x = 1`:

    >>> import numpy as np
    >>> from scipy.special import chebys, chebyu
    >>> np.isclose(chebys(3)(1), -1.0)
    True

    The polynomial :math:`S_n` is a scaled Chebyshev polynomial of the
    second kind:

    >>> x = np.linspace(-2, 2, 5)
    >>> np.allclose(chebys(3)(x), chebyu(3)(x/2))
    True

    Plot :math:`S_n` for several values of :math:`n`:

    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(-2, 2, 400)
    >>> fig, ax = plt.subplots()
    >>> for n in range(4):
    ...     ax.plot(x, chebys(n)(x), label=rf"$S_{n}$")
    >>> ax.set_title(r"Chebyshev polynomials $S_n$")
    >>> ax.set_xlabel("x")
    >>> ax.legend(loc="best")
    >>> plt.show()
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")

    if n == 0:
        n1 = n + 1
    else:
        n1 = n
    x, w = roots_chebys(n1)
    if n == 0:
        x, w = [], []
    hn = pi
    kn = 1.0
    p = orthopoly1d(x, w, hn, kn,
                    wfunc=lambda x: sqrt(1 - x * x / 4.0),
                    limits=(-2, 2), monic=monic)
    if not monic:
        factor = (n + 1.0) / p(2)
        p._scale(factor)
        p.__dict__['_eval_func'] = lambda x: _ufuncs.eval_chebys(n, x)
    return p

