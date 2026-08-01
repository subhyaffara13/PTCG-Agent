
def polyroots(coef, *, xp):
    """numpy.roots, best-effor replacement
    """
    if coef.shape[0] < 2:
        return xp.asarray([], dtype=coef.dtype)

    root_func = getattr(xp, 'roots', None)
    if root_func:
        # NB: cupy.roots is broken in CuPy 13.x, but CuPy is handled via delegation
        # so we never hit this code path with xp being cupy
        return root_func(coef)

    # companion matrix
    n = coef.shape[0]
    a = xp.eye(n - 1, n - 1, k=-1, dtype=coef.dtype)
    a[:, -1] = -xp.flip(coef[1:]) / coef[0]

    # non-symmetric eigenvalue problem is not in the spec but is available on e.g. torch
    if hasattr(xp.linalg, 'eigvals'):
        return xp.linalg.eigvals(a)
    else:
        import numpy as np
        return xp.asarray(np.linalg.eigvals(np.asarray(a)))


def polyroots(c):
    """
    Compute the roots of a polynomial.

    Return the roots (a.k.a. "zeros") of the polynomial

    .. math:: p(x) = \\sum_i c[i] * x^i.

    Parameters
    ----------
    c : 1-D array_like
        1-D array of polynomial coefficients.

    Returns
    -------
    out : ndarray
        Array of the roots of the polynomial. If all the roots are real,
        then `out` is also real, otherwise it is complex.

    See Also
    --------
    numpy.polynomial.chebyshev.chebroots
    numpy.polynomial.legendre.legroots
    numpy.polynomial.laguerre.lagroots
    numpy.polynomial.hermite.hermroots
    numpy.polynomial.hermite_e.hermeroots

    Notes
    -----
    The root estimates are obtained as the eigenvalues of the companion
    matrix, Roots far from the origin of the complex plane may have large
    errors due to the numerical instability of the power series for such
    values. Roots with multiplicity greater than 1 will also show larger
    errors as the value of the series near such points is relatively
    insensitive to errors in the roots. Isolated roots near the origin can
    be improved by a few iterations of Newton's method.

    Examples
    --------
    >>> import numpy.polynomial.polynomial as poly
    >>> poly.polyroots(poly.polyfromroots((-1,0,1)))
    array([-1.,  0.,  1.])
    >>> poly.polyroots(poly.polyfromroots((-1,0,1))).dtype
    dtype('float64')
    >>> j = complex(0,1)
    >>> poly.polyroots(poly.polyfromroots((-j,0,j)))
    array([  0.00000000e+00+0.j,   0.00000000e+00+1.j,   2.77555756e-17-1.j])  # may vary

    """  # noqa: E501
    # c is a trimmed copy
    [c] = pu.as_series([c])
    if len(c) < 2:
        return np.array([], dtype=c.dtype)
    if len(c) == 2:
        return np.array([-c[0] / c[1]])

    m = polycompanion(c)
    r = np.linalg.eigvals(m)
    r.sort()

    # backwards compat: return real values if possible
    from numpy.linalg._linalg import _to_real_if_imag_zero
    r = _to_real_if_imag_zero(r, m)
    return r


def polyroots(ctx, coeffs, maxsteps=50, cleanup=True, extraprec=10,
        error=False, roots_init=None):
    """
    Computes all roots (real or complex) of a given polynomial.

    The roots are returned as a sorted list, where real roots appear first
    followed by complex conjugate roots as adjacent elements. The polynomial
    should be given as a list of coefficients, in the format used by
    :func:`~mpmath.polyval`. The leading coefficient must be nonzero.

    With *error=True*, :func:`~mpmath.polyroots` returns a tuple *(roots, err)*
    where *err* is an estimate of the maximum error among the computed roots.

    **Examples**

    Finding the three real roots of `x^3 - x^2 - 14x + 24`::

        >>> from mpmath import *
        >>> mp.dps = 15; mp.pretty = True
        >>> nprint(polyroots([1,-1,-14,24]), 4)
        [-4.0, 2.0, 3.0]

    Finding the two complex conjugate roots of `4x^2 + 3x + 2`, with an
    error estimate::

        >>> roots, err = polyroots([4,3,2], error=True)
        >>> for r in roots:
        ...     print(r)
        ...
        (-0.375 + 0.59947894041409j)
        (-0.375 - 0.59947894041409j)
        >>>
        >>> err
        2.22044604925031e-16
        >>>
        >>> polyval([4,3,2], roots[0])
        (2.22044604925031e-16 + 0.0j)
        >>> polyval([4,3,2], roots[1])
        (2.22044604925031e-16 + 0.0j)

    The following example computes all the 5th roots of unity; that is,
    the roots of `x^5 - 1`::

        >>> mp.dps = 20
        >>> for r in polyroots([1, 0, 0, 0, 0, -1]):
        ...     print(r)
        ...
        1.0
        (-0.8090169943749474241 + 0.58778525229247312917j)
        (-0.8090169943749474241 - 0.58778525229247312917j)
        (0.3090169943749474241 + 0.95105651629515357212j)
        (0.3090169943749474241 - 0.95105651629515357212j)

    **Precision and conditioning**

    The roots are computed to the current working precision accuracy. If this
    accuracy cannot be achieved in ``maxsteps`` steps, then a
    ``NoConvergence`` exception is raised. The algorithm internally is using
    the current working precision extended by ``extraprec``. If
    ``NoConvergence`` was raised, that is caused either by not having enough
    extra precision to achieve convergence (in which case increasing
    ``extraprec`` should fix the problem) or too low ``maxsteps`` (in which
    case increasing ``maxsteps`` should fix the problem), or a combination of
    both.

    The user should always do a convergence study with regards to
    ``extraprec`` to ensure accurate results. It is possible to get
    convergence to a wrong answer with too low ``extraprec``.

    Provided there are no repeated roots, :func:`~mpmath.polyroots` can
    typically compute all roots of an arbitrary polynomial to high precision::

        >>> mp.dps = 60
        >>> for r in polyroots([1, 0, -10, 0, 1]):
        ...     print(r)
        ...
        -3.14626436994197234232913506571557044551247712918732870123249
        -0.317837245195782244725757617296174288373133378433432554879127
        0.317837245195782244725757617296174288373133378433432554879127
        3.14626436994197234232913506571557044551247712918732870123249
        >>>
        >>> sqrt(3) + sqrt(2)
        3.14626436994197234232913506571557044551247712918732870123249
        >>> sqrt(3) - sqrt(2)
        0.317837245195782244725757617296174288373133378433432554879127

    **Algorithm**

    :func:`~mpmath.polyroots` implements the Durand-Kerner method [1], which
    uses complex arithmetic to locate all roots simultaneously.
    The Durand-Kerner method can be viewed as approximately performing
    simultaneous Newton iteration for all the roots. In particular,
    the convergence to simple roots is quadratic, just like Newton's
    method.

    Although all roots are internally calculated using complex arithmetic, any
    root found to have an imaginary part smaller than the estimated numerical
    error is truncated to a real number (small real parts are also chopped).
    Real roots are placed first in the returned list, sorted by value. The
    remaining complex roots are sorted by their real parts so that conjugate
    roots end up next to each other.

    **References**

    1. http://en.wikipedia.org/wiki/Durand-Kerner_method

    """
    if len(coeffs) <= 1:
        if not coeffs or not coeffs[0]:
            raise ValueError("Input to polyroots must not be the zero polynomial")
        # Constant polynomial with no roots
        return []

    orig = ctx.prec
    tol = +ctx.eps
    with ctx.extraprec(extraprec):
        deg = len(coeffs) - 1
        # Must be monic
        lead = ctx.convert(coeffs[0])
        if lead == 1:
            coeffs = [ctx.convert(c) for c in coeffs]
        else:
            coeffs = [c/lead for c in coeffs]
        f = lambda x: ctx.polyval(coeffs, x)
        if roots_init is None:
            roots = [ctx.mpc((0.4+0.9j)**n) for n in xrange(deg)]
        else:
            roots = [None]*deg;
            deg_init = min(deg, len(roots_init))
            roots[:deg_init] = list(roots_init[:deg_init])
            roots[deg_init:] = [ctx.mpc((0.4+0.9j)**n) for n
                                in xrange(deg_init,deg)]
        err = [ctx.one for n in xrange(deg)]
        # Durand-Kerner iteration until convergence
        for step in xrange(maxsteps):
            if abs(max(err)) < tol:
                break
            for i in xrange(deg):
                p = roots[i]
                x = f(p)
                for j in range(deg):
                    if i != j:
                        try:
                            x /= (p-roots[j])
                        except ZeroDivisionError:
                            continue
                roots[i] = p - x
                err[i] = abs(x)
        if abs(max(err)) >= tol:
            raise ctx.NoConvergence("Didn't converge in maxsteps=%d steps." \
                    % maxsteps)
        # Remove small real or imaginary parts
        if cleanup:
            for i in xrange(deg):
                if abs(roots[i]) < tol:
                    roots[i] = ctx.zero
                elif abs(ctx._im(roots[i])) < tol:
                    roots[i] = roots[i].real
                elif abs(ctx._re(roots[i])) < tol:
                    roots[i] = roots[i].imag * 1j
        roots.sort(key=lambda x: (abs(ctx._im(x)), ctx._re(x)))
    if error:
        err = max(err)
        err = max(err, ctx.ldexp(1, -orig+1))
        return [+r for r in roots], +err
    else:
        return [+r for r in roots]

