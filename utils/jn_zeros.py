
def jn_zeros(n, k, method="sympy", dps=15):
    """
    Zeros of the spherical Bessel function of the first kind.

    Explanation
    ===========

    This returns an array of zeros of $jn$ up to the $k$-th zero.

    * method = "sympy": uses `mpmath.besseljzero
      <https://mpmath.org/doc/current/functions/bessel.html#mpmath.besseljzero>`_
    * method = "scipy": uses the
      `SciPy's sph_jn <https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.jn_zeros.html>`_
      and
      `newton <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html>`_
      to find all
      roots, which is faster than computing the zeros using a general
      numerical solver, but it requires SciPy and only works with low
      precision floating point numbers. (The function used with
      method="sympy" is a recent addition to mpmath; before that a general
      solver was used.)

    Examples
    ========

    >>> from sympy import jn_zeros
    >>> jn_zeros(2, 4, dps=5)
    [5.7635, 9.095, 12.323, 15.515]

    See Also
    ========

    jn, yn, besselj, besselk, bessely

    Parameters
    ==========

    n : integer
        order of Bessel function

    k : integer
        number of zeros to return


    """
    from math import pi as math_pi

    if method == "sympy":
        from mpmath import besseljzero
        from mpmath.libmp.libmpf import dps_to_prec
        prec = dps_to_prec(dps)
        return [Expr._from_mpmath(besseljzero(S(n + 0.5)._to_mpmath(prec),
                                              int(l)), prec)
                for l in range(1, k + 1)]
    elif method == "scipy":
        from scipy.optimize import newton
        try:
            from scipy.special import spherical_jn
            f = lambda x: spherical_jn(n, x)
        except ImportError:
            from scipy.special import sph_jn
            f = lambda x: sph_jn(n, x)[0][-1]
    else:
        raise NotImplementedError("Unknown method.")

    def solver(f, x):
        if method == "scipy":
            root = newton(f, x)
        else:
            raise NotImplementedError("Unknown method.")
        return root

    # we need to approximate the position of the first root:
    root = n + math_pi
    # determine the first root exactly:
    root = solver(f, root)
    roots = [root]
    for i in range(k - 1):
        # estimate the position of the next root using the last root + pi:
        root = solver(f, root + math_pi)
        roots.append(root)
    return roots


def jn_zeros(n, nt):
    r"""Compute zeros of integer-order Bessel functions Jn.

    Compute `nt` zeros of the Bessel functions :math:`J_n(x)` on the
    interval :math:`(0, \infty)`. The zeros are returned in ascending
    order. Note that this interval excludes the zero at :math:`x = 0`
    that exists for :math:`n > 0`.

    Parameters
    ----------
    n : int
        Order of Bessel function
    nt : int
        Number of zeros to return

    Returns
    -------
    ndarray
        First `nt` zeros of the Bessel function.

    See Also
    --------
    jv: Real-order Bessel functions of the first kind
    jnp_zeros: Zeros of :math:`Jn'`

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 5.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html

    Examples
    --------
    Compute the first four positive roots of :math:`J_3`.

    >>> from scipy.special import jn_zeros
    >>> jn_zeros(3, 4)
    array([ 6.3801619 ,  9.76102313, 13.01520072, 16.22346616])

    Plot :math:`J_3` and its first four positive roots. Note
    that the root located at 0 is not returned by `jn_zeros`.

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.special import jn, jn_zeros
    >>> j3_roots = jn_zeros(3, 4)
    >>> xmax = 18
    >>> xmin = -1
    >>> x = np.linspace(xmin, xmax, 500)
    >>> fig, ax = plt.subplots()
    >>> ax.plot(x, jn(3, x), label=r'$J_3$')
    >>> ax.scatter(j3_roots, np.zeros((4, )), s=30, c='r',
    ...            label=r"$J_3$_Zeros", zorder=5)
    >>> ax.scatter(0, 0, s=30, c='k',
    ...            label=r"Root at 0", zorder=5)
    >>> ax.hlines(0, 0, xmax, color='k')
    >>> ax.set_xlim(xmin, xmax)
    >>> plt.legend()
    >>> plt.show()
    """
    return jnyn_zeros(n, nt)[0]

