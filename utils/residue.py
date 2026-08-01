
def residue(expr, x, x0):
    """
    Finds the residue of ``expr`` at the point x=x0.

    The residue is defined as the coefficient of ``1/(x-x0)`` in the power series
    expansion about ``x=x0``.

    Examples
    ========

    >>> from sympy import Symbol, residue, sin
    >>> x = Symbol("x")
    >>> residue(1/x, x, 0)
    1
    >>> residue(1/x**2, x, 0)
    0
    >>> residue(2/sin(x), x, 0)
    2

    This function is essential for the Residue Theorem [1].

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Residue_theorem
    """
    # The current implementation uses series expansion to
    # calculate it. A more general implementation is explained in
    # the section 5.6 of the Bronstein's book {M. Bronstein:
    # Symbolic Integration I, Springer Verlag (2005)}. For purely
    # rational functions, the algorithm is much easier. See
    # sections 2.4, 2.5, and 2.7 (this section actually gives an
    # algorithm for computing any Laurent series coefficient for
    # a rational function). The theory in section 2.4 will help to
    # understand why the resultant works in the general algorithm.
    # For the definition of a resultant, see section 1.4 (and any
    # previous sections for more review).

    from sympy.series.order import Order
    from sympy.simplify.radsimp import collect
    expr = sympify(expr)
    if x0 != 0:
        expr = expr.subs(x, x + x0)
    for n in (0, 1, 2, 4, 8, 16, 32):
        s = expr.nseries(x, n=n)
        if not s.has(Order) or s.getn() >= 0:
            break
    s = collect(s.removeO(), x)
    if s.is_Add:
        args = s.args
    else:
        args = [s]
    res = S.Zero
    for arg in args:
        c, m = arg.as_coeff_mul(x)
        m = Mul(*m)
        if not (m in (S.One, x) or (m.is_Pow and m.exp.is_Integer)):
            raise NotImplementedError('term of unexpected form: %s' % m)
        if m == 1/x:
            res += c
    return res


def residue(b, a, tol=1e-3, rtype='avg'):
    """Compute partial-fraction expansion of b(s) / a(s).

    If `M` is the degree of numerator `b` and `N` the degree of denominator
    `a`::

              b(s)     b[0] s**(M) + b[1] s**(M-1) + ... + b[M]
      H(s) = ------ = ------------------------------------------
              a(s)     a[0] s**(N) + a[1] s**(N-1) + ... + a[N]

    then the partial-fraction expansion H(s) is defined as::

               r[0]       r[1]             r[-1]
           = -------- + -------- + ... + --------- + k(s)
             (s-p[0])   (s-p[1])         (s-p[-1])

    If there are any repeated roots (closer together than `tol`), then H(s)
    has terms like::

          r[i]      r[i+1]              r[i+n-1]
        -------- + ----------- + ... + -----------
        (s-p[i])  (s-p[i])**2          (s-p[i])**n

    This function is used for polynomials in positive powers of s or z,
    such as analog filters or digital filters in controls engineering.  For
    negative powers of z (typical for digital filters in DSP), use `residuez`.

    See Notes for details about the algorithm.

    Parameters
    ----------
    b : array_like
        Numerator polynomial coefficients.
    a : array_like
        Denominator polynomial coefficients.
    tol : float, optional
        The tolerance for two roots to be considered equal in terms of
        the distance between them. Default is 1e-3. See `unique_roots`
        for further details.
    rtype : {'avg', 'min', 'max'}, optional
        Method for computing a root to represent a group of identical roots.
        Default is 'avg'. See `unique_roots` for further details.

    Returns
    -------
    r : ndarray
        Residues corresponding to the poles. For repeated poles, the residues
        are ordered to correspond to ascending by power fractions.
    p : ndarray
        Poles ordered by magnitude in ascending order.
    k : ndarray
        Coefficients of the direct polynomial term.

    See Also
    --------
    invres, residuez, numpy.poly, unique_roots

    Notes
    -----
    The "deflation through subtraction" algorithm is used for
    computations --- method 6 in [1]_.

    The form of partial fraction expansion depends on poles multiplicity in
    the exact mathematical sense. However there is no way to exactly
    determine multiplicity of roots of a polynomial in numerical computing.
    Thus you should think of the result of `residue` with given `tol` as
    partial fraction expansion computed for the denominator composed of the
    computed poles with empirically determined multiplicity. The choice of
    `tol` can drastically change the result if there are close poles.

    References
    ----------
    .. [1] J. F. Mahoney, B. D. Sivazlian, "Partial fractions expansion: a
           review of computational methodology and efficiency", Journal of
           Computational and Applied Mathematics, Vol. 9, 1983.
    """
    b = np.asarray(b)
    a = np.asarray(a)
    if (np.issubdtype(b.dtype, np.complexfloating)
            or np.issubdtype(a.dtype, np.complexfloating)):
        b = b.astype(complex)
        a = a.astype(complex)
    else:
        b = b.astype(float)
        a = a.astype(float)

    b = np.trim_zeros(np.atleast_1d(b), 'f')
    a = np.trim_zeros(np.atleast_1d(a), 'f')

    if a.size == 0:
        raise ValueError("Denominator `a` is zero.")

    poles = np.roots(a)
    if b.size == 0:
        return np.zeros(poles.shape), _cmplx_sort(poles)[0], np.array([])

    if len(b) < len(a):
        k = np.empty(0)
    else:
        k, b = np.polydiv(b, a)

    unique_poles, multiplicity = unique_roots(poles, tol=tol, rtype=rtype)
    unique_poles, order = _cmplx_sort(unique_poles)
    multiplicity = multiplicity[order]

    residues = _compute_residues(unique_poles, multiplicity, b)

    index = 0
    for pole, mult in zip(unique_poles, multiplicity):
        poles[index:index + mult] = pole
        index += mult

    return residues / a[0], poles, k

