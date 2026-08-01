
def subresultants_amv(f, g, x):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(f, x) >= degree(g, x).

    Computes the subresultant prs of p and q in Z[x] or Q[x];
    the coefficients of the polynomials in the sequence are
    subresultants. That is, they are  determinants of appropriately
    selected submatrices of sylvester1, Sylvester's matrix of 1840.

    To compute the coefficients, no determinant evaluation takes place.
    Instead, polynomial divisions in Z[x] or Q[x] are performed, using
    the function rem_z(p, q, x);  the coefficients of the remainders
    computed this way become subresultants with the help of the
    Akritas-Malaschonok-Vigklas Theorem of 2015 and the Collins-Brown-
    Traub formula for coefficient reduction.

    If the subresultant prs is complete, then it coincides with the
    Euclidean sequence of the polynomials p, q.

    References
    ==========
    1. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``A Basic Result
    on the Theory of Subresultants.'' Serdica Journal of Computing 10 (2016), No.1, 31-48.

    2. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``Subresultant Polynomial
    remainder Sequences Obtained by Polynomial Divisions in Q[x] or in Z[x].''
    Serdica Journal of Computing 10 (2016), No.3-4, 197-217.

    """
    # make sure neither f nor g is 0
    if f == 0 or g == 0:
        return [f, g]

    # make sure proper degrees
    d0 =  degree(f, x)
    d1 =  degree(g, x)
    if d0 == 0 and d1 == 0:
        return [f, g]
    if d1 > d0:
        d0, d1 = d1, d0
        f, g = g, f
    if d0 > 0 and d1 == 0:
        return [f, g]

    # initialize
    a0 = f
    a1 = g
    subres_l = [a0, a1]
    deg_dif_p1, c = degree(a0, x) - degree(a1, x) + 1, -1

    # initialize AMV variables
    sigma1 =  LC(a1, x)                      # leading coeff of a1
    i, s = 0, 0                              # counters for remainders & odd elements
    p_odd_index_sum = 0                      # contains the sum of p_1, p_3, etc
    p0 = deg_dif_p1 - 1
    if p0 % 2 == 1:
        s += 1
    phi = floor( (s + 1) / 2 )

    # compute the first polynomial of the prs
    i += 1
    a2 = rem_z(a0, a1, x) / Abs( (-1)**deg_dif_p1 )     # first remainder
    sigma2 =  LC(a2, x)                       # leading coeff of a2
    d2 =  degree(a2, x)                       # actual degree of a2
    p1 = d1 - d2                              # degree difference

    # sgn_den is the factor, the denominator 1st fraction of (9),
    # by which a2 is multiplied to get integer coefficients
    sgn_den = compute_sign( sigma1, p0 + 1 )

    ## compute sign of the 1st fraction in formula (9) of the paper
    # numerator
    psi = i + phi + p_odd_index_sum
    num = (-1)**psi
    # denominator
    den = sgn_den

    # the sign of the determinant depends on sign(num / den) != 0
    if  sign(num / den) > 0:
        subres_l.append( a2 )
    else:
        subres_l.append( -a2 )

    # update AMV variable
    if p1 % 2 == 1:
        s += 1

    # bring in the missing power of sigma if there was gap
    if p1 - 1 > 0:
        sgn_den = sgn_den * compute_sign( sigma1, p1 - 1 )

    # main loop
    while d2 >= 1:
        phi = floor( (s + 1) / 2 )
        if i%2 == 1:
            p_odd_index_sum += p1             # p_i has odd index
        a0, a1, d0, d1 = a1, a2, d1, d2       # update polys and degrees
        p0 = p1                               # update degree difference
        i += 1
        sigma0 = -LC(a0)
        c = (sigma0**(deg_dif_p1 - 1)) / (c**(deg_dif_p1 - 2))
        deg_dif_p1 = degree(a0, x) - d2 + 1
        a2 = rem_z(a0, a1, x) / Abs( (c**(deg_dif_p1 - 1)) * sigma0 )
        sigma3 =  LC(a2, x)                   # leading coeff of a2
        d2 =  degree(a2, x)                   # actual degree of a2
        p1 = d1 - d2                          # degree difference
        psi = i + phi + p_odd_index_sum

        # update variables
        sigma1, sigma2 = sigma2, sigma3

        # new sgn_den
        sgn_den = compute_sign( sigma1, p0 + 1 ) * sgn_den

        # compute the sign of the first fraction in formula (9) of the paper
        # numerator
        num = (-1)**psi
        # denominator
        den = sgn_den

        # the sign of the determinant depends on sign( num / den ) != 0
        if  sign(num / den) > 0:
            subres_l.append( a2 )
        else:
            subres_l.append( -a2 )

        # update AMV variable
        if p1 % 2 ==1:
            s += 1

        # bring in the missing power of sigma if there was gap
        if p1 - 1 > 0:
            sgn_den = sgn_den * compute_sign( sigma1, p1 - 1 )

    # gcd is of degree > 0 ?
    m = len(subres_l)
    if subres_l[m - 1] == nan or subres_l[m - 1] == 0:
        subres_l.pop(m - 1)

    return subres_l

