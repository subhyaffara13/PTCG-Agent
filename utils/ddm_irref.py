
def ddm_irref(a, _partial_pivot=False):
    """In-place reduced row echelon form of a matrix.

    Compute the reduced row echelon form of $a$. Modifies $a$ in place and
    returns a list of the pivot columns.

    Uses naive Gauss-Jordan elimination in the ground domain which must be a
    field.

    This routine is only really suitable for use with simple field domains like
    :ref:`GF(p)`, :ref:`QQ` and :ref:`QQ(a)` although even for :ref:`QQ` with
    larger matrices it is possibly more efficient to use fraction free
    approaches.

    This method is not suitable for use with rational function fields
    (:ref:`K(x)`) because the elements will blowup leading to costly gcd
    operations. In this case clearing denominators and using fraction free
    approaches is likely to be more efficient.

    For inexact numeric domains like :ref:`RR` and :ref:`CC` pass
    ``_partial_pivot=True`` to use partial pivoting to control rounding errors.

    Examples
    ========

    >>> from sympy.polys.matrices.dense import ddm_irref
    >>> from sympy import QQ
    >>> M = [[QQ(1), QQ(2), QQ(3)], [QQ(4), QQ(5), QQ(6)]]
    >>> pivots = ddm_irref(M)
    >>> M
    [[1, 0, -1], [0, 1, 2]]
    >>> pivots
    [0, 1]

    See Also
    ========

    sympy.polys.matrices.domainmatrix.DomainMatrix.rref
        Higher level interface to this routine.
    ddm_irref_den
        The fraction free version of this routine.
    sdm_irref
        A sparse version of this routine.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Row_echelon_form#Reduced_row_echelon_form
    """
    # We compute aij**-1 below and then use multiplication instead of division
    # in the innermost loop. The domain here is a field so either operation is
    # defined. There are significant performance differences for some domains
    # though. In the case of e.g. QQ or QQ(x) inversion is free but
    # multiplication and division have the same cost so it makes no difference.
    # In cases like GF(p), QQ<sqrt(2)>, RR or CC though multiplication is
    # faster than division so reusing a precomputed inverse for many
    # multiplications can be a lot faster. The biggest win is QQ<a> when
    # deg(minpoly(a)) is large.
    #
    # With domains like QQ(x) this can perform badly for other reasons.
    # Typically the initial matrix has simple denominators and the
    # fraction-free approach with exquo (ddm_irref_den) will preserve that
    # property throughout. The method here causes denominator blowup leading to
    # expensive gcd reductions in the intermediate expressions. With many
    # generators like QQ(x,y,z,...) this is extremely bad.
    #
    # TODO: Use a nontrivial pivoting strategy to control intermediate
    # expression growth. Rearranging rows and/or columns could defer the most
    # complicated elements until the end. If the first pivot is a
    # complicated/large element then the first round of reduction will
    # immediately introduce expression blowup across the whole matrix.

    # a is (m x n)
    m = len(a)
    if not m:
        return []
    n = len(a[0])

    i = 0
    pivots = []

    for j in range(n):
        # Proper pivoting should be used for all domains for performance
        # reasons but it is only strictly needed for RR and CC (and possibly
        # other domains like RR(x)). This path is used by DDM.rref() if the
        # domain is RR or CC. It uses partial (row) pivoting based on the
        # absolute value of the pivot candidates.
        if _partial_pivot:
            ip = max(range(i, m), key=lambda ip: abs(a[ip][j]))
            a[i], a[ip] = a[ip], a[i]

        # pivot
        aij = a[i][j]

        # zero-pivot
        if not aij:
            for ip in range(i+1, m):
                aij = a[ip][j]
                # row-swap
                if aij:
                    a[i], a[ip] = a[ip], a[i]
                    break
            else:
                # next column
                continue

        # normalise row
        ai = a[i]
        aijinv = aij**-1
        for l in range(j, n):
            ai[l] *= aijinv # ai[j] = one

        # eliminate above and below to the right
        for k, ak in enumerate(a):
            if k == i or not ak[j]:
                continue
            akj = ak[j]
            ak[j] -= akj # ak[j] = zero
            for l in range(j+1, n):
                ak[l] -= akj * ai[l]

        # next row
        pivots.append(j)
        i += 1

        # no more rows?
        if i >= m:
            break

    return pivots

