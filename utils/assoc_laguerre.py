
def assoc_laguerre(x, n, k=0.0):
    r"""Compute the generalized (associated) Laguerre polynomial of degree :math:`n`
    and order :math:`k`.

    This function evaluates the generalized Laguerre polynomial

    .. math::

        L^{(k)}_n(x).

    The polynomial is orthogonal over :math:`[0, \infty)` with weight
    function

    .. math::

        e^{-x}x^k

    for :math:`k > -1`.

    Parameters
    ----------
    x : float or ndarray
        Points where to evaluate the Laguerre polynomial
    n : int
        Degree of the Laguerre polynomial
    k : int
        Order of the Laguerre polynomial

    Returns
    -------
    assoc_laguerre: float or ndarray
        Associated laguerre polynomial values

    Notes
    -----
    `assoc_laguerre` is a simple wrapper around `eval_genlaguerre`, with
    reversed argument order ``(x, n, k=0.0) --> (n, k, x)``.

    Examples
    --------
    Evaluate the associated Laguerre polynomial :math:`L_3^{(2)}` at
    :math:`x = 1`:

    >>> import numpy as np
    >>> from scipy.special import assoc_laguerre, eval_genlaguerre
    >>> np.isclose(assoc_laguerre(1, 3, 2), 7/3)
    True

    `assoc_laguerre` is equivalent to `eval_genlaguerre` with reversed
    argument order:

    >>> x = np.linspace(0, 5, 6)
    >>> np.allclose(assoc_laguerre(x, 3, 2), eval_genlaguerre(3, 2, x))
    True

    Plot :math:`L_3^{(k)}` for several values of :math:`k`:

    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(0, 8, 400)
    >>> fig, ax = plt.subplots()
    >>> for k in range(3):
    ...     ax.plot(x, assoc_laguerre(x, 3, k), label=rf"$k={k}$")
    >>> ax.set_title(r"Associated Laguerre polynomials $L_3^{(k)}$")
    >>> ax.set_xlabel("x")
    >>> ax.legend(loc="best")
    >>> plt.show()

    """
    return _ufuncs.eval_genlaguerre(n, k, x)

