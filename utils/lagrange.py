import os

def lagrange(x, w):
    r"""
    Return a Lagrange interpolating polynomial.

    Given two 1-D arrays `x` and `w,` returns the Lagrange interpolating
    polynomial through the points ``(x, w)``.

    Warning: This implementation is numerically unstable. Do not expect to
    be able to use more than about 20 points even if they are chosen optimally.

    .. deprecated:: 1.18.0
        This function is deprecated and will be removed in SciPy 1.20.0. Use
        `scipy.interpolate.BarycentricInterpolator` instead.

    Parameters
    ----------
    x : array_like
        `x` represents the x-coordinates of a set of datapoints.
    w : array_like
        `w` represents the y-coordinates of a set of datapoints, i.e., f(`x`).

    Returns
    -------
    lagrange : `numpy.poly1d` instance
        The Lagrange interpolating polynomial.

    Notes
    -----
    The name of this function refers to the fact that the returned object represents
    a Lagrange polynomial, the unique polynomial of lowest degree that interpolates
    a given set of data [1]_. It computes the polynomial using Newton's divided
    differences formula [2]_; that is, it works with Newton basis polynomials rather
    than Lagrange basis polynomials. For numerical calculations, the barycentric form
    of Lagrange interpolation (`scipy.interpolate.BarycentricInterpolator`) is
    typically more appropriate.

    References
    ----------
    .. [1] Lagrange polynomial. *Wikipedia*.
           https://en.wikipedia.org/wiki/Lagrange_polynomial
    .. [2] Newton polynomial. *Wikipedia*.
           https://en.wikipedia.org/wiki/Newton_polynomial

    Examples
    --------
    Interpolate :math:`f(x) = x^3` by 3 points.

    >>> import numpy as np
    >>> from scipy.interpolate import lagrange
    >>> x = np.array([0, 1, 2])
    >>> y = x**3
    >>> poly = lagrange(x, y)

    Since there are only 3 points, the Lagrange polynomial has degree 2. Explicitly,
    it is given by

    .. math::

        \begin{aligned}
            L(x) &= 1\times \frac{x (x - 2)}{-1} + 8\times \frac{x (x-1)}{2} \\
                 &= x (-2 + 3x)
        \end{aligned}

    >>> from numpy.polynomial.polynomial import Polynomial
    >>> Polynomial(poly.coef[::-1]).coef
    array([ 0., -2.,  3.])

    >>> import matplotlib.pyplot as plt
    >>> x_new = np.arange(0, 2.1, 0.1)
    >>> plt.scatter(x, y, label='data')
    >>> plt.plot(x_new, Polynomial(poly.coef[::-1])(x_new), label='Polynomial')
    >>> plt.plot(x_new, 3*x_new**2 - 2*x_new + 0*x_new,
    ...          label=r"$3 x^2 - 2 x$", linestyle='-.')
    >>> plt.legend()
    >>> plt.show()

    """
    _warn_skips = (os.path.dirname(__file__),)
    msg = ("`lagrange` is deprecated and will be removed in SciPy 1.20.0. Use "
           "`scipy.interpolate.BarycentricInterpolator` instead.")
    warnings.warn(msg, DeprecationWarning, skip_file_prefixes=_warn_skips)
    M = len(x)
    p = poly1d(0.0)
    for j in range(M):
        pt = poly1d(w[j])
        for k in range(M):
            if k == j:
                continue
            fac = x[j]-x[k]
            pt *= poly1d([1.0, -x[k]])/fac
        p += pt
    return p

