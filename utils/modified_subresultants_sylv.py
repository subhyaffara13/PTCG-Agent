
def modified_subresultants_sylv(f, g, x):
    """
    The input polynomials f, g are in Z[x] or in Q[x]. It is assumed
    that deg(f) >= deg(g).

    Computes the modified subresultant polynomial remainder sequence (prs)
    of f, g by evaluating determinants of appropriately selected
    submatrices of sylvester(f, g, x, 2). The dimensions of the
    latter are (2*deg(f)) x (2*deg(f)).

    Each coefficient is computed by evaluating the determinant of the
    corresponding submatrix of sylvester(f, g, x, 2).

    If the modified subresultant prs is complete, then the output coincides
    with the Sturmian sequence of the polynomials f, g.

    References:
    ===========
    1. A. G. Akritas,G.I. Malaschonok and P.S. Vigklas:
    Sturm Sequences and Modified Subresultant Polynomial Remainder
    Sequences. Serdica Journal of Computing, Vol. 8, No 1, 29--46, 2014.

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

    SR_L = [f, g]      # modified subresultant list

    # form matrix sylvester(f, g, x, 2)
    S = sylvester(f, g, x, 2)

    # pick appropriate submatrices of S
    # and form modified subresultant polys
    j = m - 1

    while j > 0:
        # delete last 2*j rows of pairs of coeffs of f, g
        Sp = S[0:2*n - 2*j, :]  # copy of first 2*n - 2*j rows of S

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

