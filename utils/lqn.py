
def lqn(n, z):
    """Legendre functions of the second kind.

    Compute sequence of Legendre functions of the second kind, ``Qn(z)`` and
    derivatives for all degrees from 0 to `n` (inclusive).
    Returns two arrays of size ``(n+1,) + z.shape`` containing ``Qn(z)`` and
    ``Qn'(z)``.

    Parameters
    ----------
    n : int
        Maximum degree of the Legendre functions.
    z : array_like, complex
        Real or complex input values.

    Returns
    -------
    Qn_z : ndarray, shape (n+1,) + shape(z)
        Values for all degrees ``0..n``
    Qn_d_z : ndarray, shape (n+1,) + shape(z)
        Derivatives for all degrees ``0..n``

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html

    Examples
    --------
    Compute :math:`Q_n(x)` and its derivatives on an interval.

    >>> import numpy as np
    >>> from scipy.special import lqn
    >>> import matplotlib.pyplot as plt

    >>> xs = np.linspace(-2, 2, 200)
    >>> n_max = 3
    >>> Qn, dQn = lqn(n_max, xs)

    Plot the Legendre functions of the second kind :math:`Q_n(x)`.

    >>> fig, ax = plt.subplots()
    >>> ax.plot(xs, Qn.T, "-")
    >>> ax.set_xlabel(r"$x$")
    >>> ax.set_ylabel(r"$Q_n(x)$")
    >>> ax.legend([fr"$n={n}$" for n in range(n_max + 1)])
    >>> plt.show()

    Plot the derivatives :math:`Q_n'(x)`.

    >>> fig, ax = plt.subplots()
    >>> ax.plot(xs, dQn.T, "-")
    >>> ax.set_xlabel(r"$x$")
    >>> ax.set_ylabel(r"$Q_n'(x)$")
    >>> ax.legend([fr"$n={n}$" for n in range(n_max + 1)])
    >>> plt.show()
    """
    n = _nonneg_int_or_fail(n, 'n', strict=False)
    if (n < 1):
        n1 = 1
    else:
        n1 = n

    z = np.asarray(z)
    if (not np.issubdtype(z.dtype, np.inexact)):
        z = z.astype(float)

    if np.iscomplexobj(z):
        qn = np.empty((n1 + 1,) + z.shape, dtype=np.complex128)
    else:
        qn = np.empty((n1 + 1,) + z.shape, dtype=np.float64)
    qd = np.empty_like(qn)
    if (z.ndim == 0):
        _lqn(z, out=(qn, qd))
    else:
          # new axes must be last for the ufunc
        _lqn(z,
             out=(np.moveaxis(qn, 0, -1),
                  np.moveaxis(qd, 0, -1)))

    return qn[:(n+1)], qd[:(n+1)]

