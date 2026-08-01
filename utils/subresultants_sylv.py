
def subresultants_sylv(f, g, x):
    """
    The input polynomials f, g are in Z[x] or in Q[x]. It is assumed
    that deg(f) >= deg(g).

    Computes the subresultant polynomial remainder sequence (prs)
    of f, g by evaluating determinants of appropriately selected
    submatrices of sylvester(f, g, x, 1). The dimensions of the
    latter are (deg(f) + deg(g)) x (deg(f) + deg(g)).

    Each coefficient is computed by evaluating the determinant of the
    corresponding submatrix of sylvester(f, g, x, 1).

    If the subresultant prs is complete, then the output coincides
    with the Euclidean sequence of the polynomials f, g.

    References:
    ===========
    1. G.M.Diaz-Toca,L.Gonzalez-Vega: Various New Expressions for Subresultants
    and Their Applications. Appl. Algebra in Engin., Communic. and Comp.,
    Vol. 15, 233-266, 2004.

    """

    # make sure neither f nor g is 0
    if f == 0 or g == 0:
        return [f, g]

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

    # form matrix sylvester(f, g, x, 1)
    S = sylvester(f, g, x, 1)

    # pick appropriate submatrices of S
    # and form subresultant polys
    j = m - 1

    while j > 0:
        Sp = S[:, :]  # copy of S
        # delete last j rows of coeffs of g
        for ind in range(m + n - j, m + n):
            Sp.row_del(m + n - j)
        # delete last j rows of coeffs of f
        for ind in range(m - j, m):
            Sp.row_del(m - j)

        # evaluate determinants and form coefficients list
        coeff_L, k, l = [], Sp.rows, 0
        while l <= j:
            coeff_L.append(Sp[:, 0:k].det())
            Sp.col_swap(k - 1, k + l)
            l += 1

        # form poly and append to SP_L
        SR_L.append(Poly(coeff_L, x).as_expr())
        j -= 1

    # j = 0
    SR_L.append(S.det())

    return process_matrix_output(SR_L, x)

