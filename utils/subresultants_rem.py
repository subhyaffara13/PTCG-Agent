
def subresultants_rem(p, q, x):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the subresultant prs of p and q in Z[x] or Q[x];
    the coefficients of the polynomials in the sequence are
    subresultants. That is, they are  determinants of appropriately
    selected submatrices of sylvester1, Sylvester's matrix of 1840.

    To compute the coefficients polynomial divisions in Q[x] are
    performed, using the function rem(p, q, x). The coefficients
    of the remainders computed this way become subresultants by evaluating
    one subresultant per remainder --- that of the leading coefficient.
    This way we obtain the correct sign and value of the leading coefficient
    of the remainder and we easily ``force'' the rest of the coefficients
    to become subresultants.

    If the subresultant prs is complete, then it coincides with the
    Euclidean sequence of the polynomials p, q.

    References
    ==========
    1. Akritas, A. G.:``Three New Methods for Computing Subresultant
    Polynomial Remainder Sequences (PRS's).'' Serdica Journal of Computing 9(1) (2015), 1-26.

    """
    # make sure neither p nor q is 0
    if p == 0 or q == 0:
        return [p, q]

    # make sure proper degrees
    f, g = p, q
    n = deg_f = degree(f, x)
    m = deg_g = degree(g, x)
    if n == 0 and m == 0:
        return [f, g]
    if n < m:
        n, m, deg_f, deg_g, f, g = m, n, deg_g, deg_f, g, f
    if n > 0 and m == 0:
        return [f, g]

    # initialize
    s1 = sylvester(f, g, x, 1)
    sr_list = [f, g]      # subresultant list

    # main loop
    while deg_g > 0:
        r = rem(p, q, x)
        d = degree(r, x)
        if d < 0:
            return sr_list

        # make coefficients subresultants evaluating ONE determinant
        exp_deg = deg_g - 1          # expected degree
        sign_value = correct_sign(n, m, s1, exp_deg, exp_deg - d)
        r = simplify((r / LC(r, x)) * sign_value)

        # append poly with subresultant coeffs
        sr_list.append(r)

        # update degrees and polys
        deg_f, deg_g = deg_g, d
        p, q = q, r

    # gcd is of degree > 0 ?
    m = len(sr_list)
    if sr_list[m - 1] == nan or sr_list[m - 1] == 0:
        sr_list.pop(m - 1)

    return sr_list

