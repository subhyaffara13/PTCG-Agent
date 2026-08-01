
def spherical_yn(n, z, derivative=False):
    r"""Spherical Bessel function of the second kind or its derivative.

    Defined as [1]_,

    .. math:: y_n(z) = \sqrt{\frac{\pi}{2z}} Y_{n + 1/2}(z),

    where :math:`Y_n` is the Bessel function of the second kind.

    Parameters
    ----------
    n : int, array_like
        Order of the Bessel function (n >= 0).
    z : complex or float, array_like
        Argument of the Bessel function.
    derivative : bool, optional
        If True, the value of the derivative (rather than the function
        itself) is returned.

    Returns
    -------
    yn : ndarray
        Value or derivative of spherical Bessel function of the second kind.

    Notes
    -----
    For real arguments, the function is computed using the ascending
    recurrence [2]_.  For complex arguments, the definitional relation to
    the cylindrical Bessel function of the second kind is used.

    The derivative is computed using the relations [3]_,

    .. math::
        y_n' = y_{n-1} - \frac{n + 1}{z} y_n.

        y_0' = -y_1


    .. versionadded:: 0.18.0

    References
    ----------
    .. [1] https://dlmf.nist.gov/10.47.E4
    .. [2] https://dlmf.nist.gov/10.51.E1
    .. [3] https://dlmf.nist.gov/10.51.E2
    .. [AS] Milton Abramowitz and Irene A. Stegun, eds.
        Handbook of Mathematical Functions with Formulas,
        Graphs, and Mathematical Tables. New York: Dover, 1972.

    Examples
    --------
    The spherical Bessel functions of the second kind :math:`y_n` accept
    both real and complex second argument. They can return a complex type:

    >>> from scipy.special import spherical_yn
    >>> spherical_yn(0, 3+5j)
    (8.022343088587197-9.880052589376795j)
    >>> type(spherical_yn(0, 3+5j))
    <class 'numpy.complex128'>

    We can verify the relation for the derivative from the Notes
    for :math:`n=3` in the interval :math:`[1, 2]`:

    >>> import numpy as np
    >>> x = np.arange(1.0, 2.0, 0.01)
    >>> np.allclose(spherical_yn(3, x, True),
    ...             spherical_yn(2, x) - 4/x * spherical_yn(3, x))
    True

    The first few :math:`y_n` with real argument:

    >>> import matplotlib.pyplot as plt
    >>> x = np.arange(0.0, 10.0, 0.01)
    >>> fig, ax = plt.subplots()
    >>> ax.set_ylim(-2.0, 1.0)
    >>> ax.set_title(r'Spherical Bessel functions $y_n$')
    >>> for n in np.arange(0, 4):
    ...     ax.plot(x, spherical_yn(n, x), label=rf'$y_{n}$')
    >>> plt.legend(loc='best')
    >>> plt.show()

    """
    n = np.asarray(n, dtype=np.dtype("long"))
    if derivative:
        return _spherical_yn_d(n, z)
    else:
        return _spherical_yn(n, z)

