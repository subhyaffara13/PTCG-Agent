
def all_roots(f, multiple=True, radicals=True, extension=False):
    """
    Returns the real and complex roots of ``f`` with multiplicities.

    Explanation
    ===========

    Finds all real and complex roots of a univariate polynomial with rational
    coefficients of any degree exactly. The roots are represented in the form
    given by :func:`~.rootof`. This is equivalent to using :func:`~.rootof` to
    find each of the indexed roots.

    Examples
    ========

    >>> from sympy import all_roots
    >>> from sympy.abc import x, y

    >>> print(all_roots(x**3 + 1))
    [-1, 1/2 - sqrt(3)*I/2, 1/2 + sqrt(3)*I/2]

    Simple radical formulae are used in some cases but the cubic and quartic
    formulae are avoided. Instead most non-rational roots will be represented
    as :class:`~.ComplexRootOf`:

    >>> print(all_roots(x**3 + x + 1))
    [CRootOf(x**3 + x + 1, 0), CRootOf(x**3 + x + 1, 1), CRootOf(x**3 + x + 1, 2)]

    All roots of any polynomial with rational coefficients of any degree can be
    represented using :py:class:`~.ComplexRootOf`. The use of
    :py:class:`~.ComplexRootOf` bypasses limitations on the availability of
    radical formulae for quintic and higher degree polynomials _[1]:

    >>> p = x**5 - x - 1
    >>> for r in all_roots(p): print(r)
    CRootOf(x**5 - x - 1, 0)
    CRootOf(x**5 - x - 1, 1)
    CRootOf(x**5 - x - 1, 2)
    CRootOf(x**5 - x - 1, 3)
    CRootOf(x**5 - x - 1, 4)
    >>> [r.evalf(3) for r in all_roots(p)]
    [1.17, -0.765 - 0.352*I, -0.765 + 0.352*I, 0.181 - 1.08*I, 0.181 + 1.08*I]

    Irrational algebraic coefficients are handled by :func:`all_roots`
    if `extension=True` is set.

    >>> from sympy import sqrt, expand
    >>> p = expand((x - sqrt(2))*(x - sqrt(3)))
    >>> print(p)
    x**2 - sqrt(3)*x - sqrt(2)*x + sqrt(6)
    >>> all_roots(p)
    Traceback (most recent call last):
    ...
    NotImplementedError: sorted roots not supported over EX
    >>> all_roots(p, extension=True)
    [sqrt(2), sqrt(3)]

    Algebraic coefficients can be complex as well.

    >>> from sympy import I
    >>> all_roots(x**2 - I, extension=True)
    [-sqrt(2)/2 - sqrt(2)*I/2, sqrt(2)/2 + sqrt(2)*I/2]
    >>> all_roots(x**2 - sqrt(2)*I, extension=True)
    [-2**(3/4)/2 - 2**(3/4)*I/2, 2**(3/4)/2 + 2**(3/4)*I/2]

    Transcendental coefficients cannot currently be handled by
    :func:`all_roots`. In the case of algebraic or transcendental coefficients
    :func:`~.ground_roots` might be able to find some roots by factorisation:

    >>> from sympy import ground_roots
    >>> ground_roots(p, x, extension=True)
    {sqrt(2): 1, sqrt(3): 1}

    If the coefficients are numeric then :func:`~.nroots` can be used to find
    all roots approximately:

    >>> from sympy import nroots
    >>> nroots(p, 5)
    [1.4142, 1.732]

    If the coefficients are symbolic then :func:`sympy.polys.polyroots.roots`
    or :func:`~.ground_roots` should be used instead:

    >>> from sympy import roots, ground_roots
    >>> p = x**2 - 3*x*y + 2*y**2
    >>> roots(p, x)
    {y: 1, 2*y: 1}
    >>> ground_roots(p, x)
    {y: 1, 2*y: 1}

    Parameters
    ==========

    f : :class:`~.Expr` or :class:`~.Poly`
        A univariate polynomial with rational (or ``Float``) coefficients.
    multiple : ``bool`` (default ``True``).
        Whether to return a ``list`` of roots or a list of root/multiplicity
        pairs.
    radicals : ``bool`` (default ``True``)
        Use simple radical formulae rather than :py:class:`~.ComplexRootOf` for
        some irrational roots.
    extension: ``bool`` (default ``False``)
        Whether to construct an algebraic extension domain before computing
        the roots. Setting to ``True`` is necessary for finding roots of a
        polynomial with (irrational) algebraic coefficients but can be slow.

    Returns
    =======

    A list of :class:`~.Expr` (usually :class:`~.ComplexRootOf`) representing
    the roots is returned with each root repeated according to its multiplicity
    as a root of ``f``. The roots are always uniquely ordered with real roots
    coming before complex roots. The real roots are in increasing order.
    Complex roots are ordered by increasing real part and then increasing
    imaginary part.

    If ``multiple=False`` is passed then a list of root/multiplicity pairs is
    returned instead.

    If ``radicals=False`` is passed then all roots will be represented as
    either rational numbers or :class:`~.ComplexRootOf`.

    See also
    ========

    Poly.all_roots:
        The underlying :class:`Poly` method used by :func:`~.all_roots`.
    rootof:
        Compute a single numbered root of a univariate polynomial.
    real_roots:
        Compute all the real roots using :func:`~.rootof`.
    ground_roots:
        Compute some roots in the ground domain by factorisation.
    nroots:
        Compute all roots using approximate numerical techniques.
    sympy.polys.polyroots.roots:
        Compute symbolic expressions for roots using radical formulae.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Abel%E2%80%93Ruffini_theorem
    """
    try:
        if isinstance(f, Poly):
            if extension and not f.domain.is_AlgebraicField:
                F = Poly(f.expr, extension=True)
            else:
                F = f
        else:
            if extension:
                F = Poly(f, extension=True)
            else:
                F = Poly(f, greedy=False)

        if not isinstance(f, Poly) and not F.gen.is_Symbol:
            # root of sin(x) + 1 is -1 but when someone
            # passes an Expr instead of Poly they may not expect
            # that the generator will be sin(x), not x
            raise PolynomialError("generator must be a Symbol")
    except GeneratorsNeeded:
        raise PolynomialError(
            "Cannot compute real roots of %s, not a polynomial" % f)

    return F.all_roots(multiple=multiple, radicals=radicals)

