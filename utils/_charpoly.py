
def _charpoly(M, x='lambda', simplify=_simplify):
    """Computes characteristic polynomial det(x*I - M) where I is
    the identity matrix.

    A PurePoly is returned, so using different variables for ``x`` does
    not affect the comparison or the polynomials:

    Parameters
    ==========

    x : string, optional
        Name for the "lambda" variable, defaults to "lambda".

    simplify : function, optional
        Simplification function to use on the characteristic polynomial
        calculated. Defaults to ``simplify``.

    Examples
    ========

    >>> from sympy import Matrix
    >>> from sympy.abc import x, y
    >>> M = Matrix([[1, 3], [2, 0]])
    >>> M.charpoly()
    PurePoly(lambda**2 - lambda - 6, lambda, domain='ZZ')
    >>> M.charpoly(x) == M.charpoly(y)
    True
    >>> M.charpoly(x) == M.charpoly(y)
    True

    Specifying ``x`` is optional; a symbol named ``lambda`` is used by
    default (which looks good when pretty-printed in unicode):

    >>> M.charpoly().as_expr()
    lambda**2 - lambda - 6

    And if ``x`` clashes with an existing symbol, underscores will
    be prepended to the name to make it unique:

    >>> M = Matrix([[1, 2], [x, 0]])
    >>> M.charpoly(x).as_expr()
    _x**2 - _x - 2*x

    Whether you pass a symbol or not, the generator can be obtained
    with the gen attribute since it may not be the same as the symbol
    that was passed:

    >>> M.charpoly(x).gen
    _x
    >>> M.charpoly(x).gen == x
    False

    Notes
    =====

    The Samuelson-Berkowitz algorithm is used to compute
    the characteristic polynomial efficiently and without any
    division operations.  Thus the characteristic polynomial over any
    commutative ring without zero divisors can be computed.

    If the determinant det(x*I - M) can be found out easily as
    in the case of an upper or a lower triangular matrix, then
    instead of Samuelson-Berkowitz algorithm, eigenvalues are computed
    and the characteristic polynomial with their help.

    See Also
    ========

    det
    """

    if not M.is_square:
        raise NonSquareMatrixError()

    # Use DomainMatrix. We are already going to convert this to a Poly so there
    # is no need to worry about expanding powers etc. Also since this algorithm
    # does not require division or zero detection it is fine to use EX.
    #
    # M.to_DM() will fall back on EXRAW rather than EX. EXRAW is a lot faster
    # for elementary arithmetic because it does not call cancel for each
    # operation but it generates large unsimplified results that are slow in
    # the subsequent call to simplify. Using EX instead is faster overall
    # but at least in some cases EXRAW+simplify gives a simpler result so we
    # preserve that existing behaviour of charpoly for now...
    dM = M.to_DM()

    K = dM.domain

    cp = dM.charpoly()

    x = uniquely_named_symbol(x, [M], modify=lambda s: '_' + s)

    if K.is_EXRAW or simplify is not _simplify:
        # XXX: Converting back to Expr is expensive. We only do it if the
        # caller supplied a custom simplify function for backwards
        # compatibility or otherwise if the domain was EX. For any other domain
        # there should be no benefit in simplifying at this stage because Poly
        # will put everything into canonical form anyway.
        berk_vector = [K.to_sympy(c) for c in cp]
        berk_vector = [simplify(a) for a in berk_vector]
        p = PurePoly(berk_vector, x)

    else:
        # Convert from the list of domain elements directly to Poly.
        p = PurePoly(cp, x, domain=K)

    return p

