
def modified_subresultants_bezout(p, q, x):
    """
    The input polynomials p, q are in Z[x] or in Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the modified subresultant polynomial remainder sequence
    of p, q by evaluating determinants of appropriately selected
    submatrices of bezout(p, q, x, 'prs'). The dimensions of the
    latter are deg(p) x deg(p).

    Each coefficient is computed by evaluating the determinant of the
    corresponding submatrix of bezout(p, q, x, 'prs').

    bezout(p, q, x, 'prs') is used instead of sylvester(p, q, x, 2),
    Sylvester's matrix of 1853, because the dimensions of the latter
    are 2*deg(p) x 2*deg(p).

    If the modified subresultant prs is complete, and LC( p ) > 0, the output
    coincides with the (generalized) Sturm's sequence of the polynomials p, q.

    References
    ==========
    1. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``Sturm Sequences
    and Modified Subresultant Polynomial Remainder Sequences.''
    Serdica Journal of Computing, Vol. 8, No 1, 29-46, 2014.

    2. G.M.Diaz-Toca,L.Gonzalez-Vega: Various New Expressions for Subresultants
    and Their Applications. Appl. Algebra in Engin., Communic. and Comp.,
    Vol. 15, 233-266, 2004.


    """
    # make sure neither p nor q is 0
    if p == 0 or q == 0:
        return [p, q]

    f, g = p, q
    n = degF = degree(f, x)
    m = degG = degree(g, x)

    # make sure proper degrees
    if n == 0 and m == 0:
        return [f, g]
    if n < m:
        n, m, degF, degG, f, g = m, n, degG, degF, g, f
    if n > 0 and m == 0:
        return [f, g]

    SR_L = [f, g]      # subresultant list

    # form the bezout matrix
    B = bezout(f, g, x, 'prs')

    # pick appropriate submatrices of B
    # and form subresultant polys
    if degF > degG:
        j = 2
    if degF == degG:
        j = 1
    while j <= degF:
        M = B[0:j, :]
        k, coeff_L = j - 1, []
        while k <= degF - 1:
            coeff_L.append(M[:, 0:j].det())
            if k < degF - 1:
                M.col_swap(j - 1, k + 1)
            k = k + 1

        ## Theorem 2.1 in the paper by Toca & Vega 2004 is _not needed_
        ## in this case since
        ## the bezout matrix is equivalent to sylvester2
        SR_L.append(( Poly(coeff_L, x)).as_expr())
        j = j + 1

    return process_matrix_output(SR_L, x)

