
def dup_sign_variations(f, K):
    """
    Compute the number of sign variations of ``f`` in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_sign_variations(x**4 - x**2 - x + 1)
    2

    """
    def is_negative_sympy(a):
        if not a:
            # XXX: requires zero equivalence testing in the domain
            return False
        else:
            # XXX: This is inefficient. It should not be necessary to use a
            # symbolic expression here at least for algebraic fields. If the
            # domain elements can be numerically evaluated to real values with
            # precision then this should work. We first need to rule out zero
            # elements though.
            return bool(K.to_sympy(a) < 0)

    # XXX: There should be a way to check for real numeric domains and
    # Domain.is_negative should be fixed to handle all real numeric domains.
    # It should not be necessary to special case all these different domains
    # in this otherwise generic function.
    if K.is_ZZ or K.is_QQ or K.is_RR:
        is_negative = K.is_negative
    elif K.is_AlgebraicField and K.ext.is_comparable:
        is_negative = is_negative_sympy
    elif ((K.is_PolynomialRing or K.is_FractionField) and len(K.symbols) == 1 and
          (K.dom.is_ZZ or K.dom.is_QQ or K.is_AlgebraicField) and
          K.symbols[0].is_transcendental and K.symbols[0].is_comparable):
        # We can handle a polynomial ring like QQ[E] if there is a single
        # transcendental generator because then zero equivalence is assured.
        is_negative = is_negative_sympy
    else:
        raise DomainError("sign variation counting not supported over %s" % K)

    prev, k = K.zero, 0

    for coeff in f:
        if is_negative(coeff*prev):
            k += 1

        if coeff:
            prev = coeff

    return k

