
def sturm_pg(p, q, x, method=0):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the (generalized) Sturm sequence of p and q in Z[x] or Q[x].
    If q = diff(p, x, 1) it is the usual Sturm sequence.

    A. If method == 0, default, the remainder coefficients of the sequence
       are (in absolute value) ``modified'' subresultants, which for non-monic
       polynomials are greater than the coefficients of the corresponding
       subresultants by the factor Abs(LC(p)**( deg(p)- deg(q))).

    B. If method == 1, the remainder coefficients of the sequence are (in
       absolute value) subresultants, which for non-monic polynomials are
       smaller than the coefficients of the corresponding ``modified''
       subresultants by the factor Abs(LC(p)**( deg(p)- deg(q))).

    If the Sturm sequence is complete, method=0 and LC( p ) > 0, the coefficients
    of the polynomials in the sequence are ``modified'' subresultants.
    That is, they are  determinants of appropriately selected submatrices of
    sylvester2, Sylvester's matrix of 1853. In this case the Sturm sequence
    coincides with the ``modified'' subresultant prs, of the polynomials
    p, q.

    If the Sturm sequence is incomplete and method=0 then the signs of the
    coefficients of the polynomials in the sequence may differ from the signs
    of the coefficients of the corresponding polynomials in the ``modified''
    subresultant prs; however, the absolute values are the same.

    To compute the coefficients, no determinant evaluation takes place. Instead,
    polynomial divisions in Q[x] are performed, using the function rem(p, q, x);
    the coefficients of the remainders computed this way become (``modified'')
    subresultants with the help of the Pell-Gordon Theorem of 1917.
    See also the function euclid_pg(p, q, x).

    References
    ==========
    1. Pell A. J., R. L. Gordon. The Modified Remainders Obtained in Finding
    the Highest Common Factor of Two Polynomials. Annals of MatheMatics,
    Second Series, 18 (1917), No. 4, 188-193.

    2. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``Sturm Sequences
    and Modified Subresultant Polynomial Remainder Sequences.''
    Serdica Journal of Computing, Vol. 8, No 1, 29-46, 2014.

    """
    # make sure neither p nor q is 0
    if p == 0 or q == 0:
        return [p, q]

    # make sure proper degrees
    d0 =  degree(p, x)
    d1 =  degree(q, x)
    if d0 == 0 and d1 == 0:
        return [p, q]
    if d1 > d0:
        d0, d1 = d1, d0
        p, q = q, p
    if d0 > 0 and d1 == 0:
        return [p,q]

    # make sure LC(p) > 0
    flag = 0
    if  LC(p,x) < 0:
        flag = 1
        p = -p
        q = -q

    # initialize
    lcf = LC(p, x)**(d0 - d1)               # lcf * subr = modified subr
    a0, a1 = p, q                           # the input polys
    sturm_seq = [a0, a1]                    # the output list
    del0 = d0 - d1                          # degree difference
    rho1 =  LC(a1, x)                       # leading coeff of a1
    exp_deg = d1 - 1                        # expected degree of a2
    a2 = - rem(a0, a1, domain=QQ)           # first remainder
    rho2 =  LC(a2,x)                        # leading coeff of a2
    d2 =  degree(a2, x)                     # actual degree of a2
    deg_diff_new = exp_deg - d2             # expected - actual degree
    del1 = d1 - d2                          # degree difference

    # mul_fac is the factor by which a2 is multiplied to
    # get integer coefficients
    mul_fac_old = rho1**(del0 + del1 - deg_diff_new)

    # append accordingly
    if method == 0:
        sturm_seq.append( simplify(lcf * a2 *  Abs(mul_fac_old)))
    else:
        sturm_seq.append( simplify( a2 *  Abs(mul_fac_old)))

    # main loop
    deg_diff_old = deg_diff_new
    while d2 > 0:
        a0, a1, d0, d1 = a1, a2, d1, d2      # update polys and degrees
        del0 = del1                          # update degree difference
        exp_deg = d1 - 1                     # new expected degree
        a2 = - rem(a0, a1, domain=QQ)        # new remainder
        rho3 =  LC(a2, x)                    # leading coeff of a2
        d2 =  degree(a2, x)                  # actual degree of a2
        deg_diff_new = exp_deg - d2          # expected - actual degree
        del1 = d1 - d2                       # degree difference

        # take into consideration the power
        # rho1**deg_diff_old that was "left out"
        expo_old = deg_diff_old               # rho1 raised to this power
        expo_new = del0 + del1 - deg_diff_new # rho2 raised to this power

        # update variables and append
        mul_fac_new = rho2**(expo_new) * rho1**(expo_old) * mul_fac_old
        deg_diff_old, mul_fac_old = deg_diff_new, mul_fac_new
        rho1, rho2 = rho2, rho3
        if method == 0:
            sturm_seq.append( simplify(lcf * a2 *  Abs(mul_fac_old)))
        else:
            sturm_seq.append( simplify( a2 *  Abs(mul_fac_old)))

    if flag:          # change the sign of the sequence
        sturm_seq = [-i for i in sturm_seq]

    # gcd is of degree > 0 ?
    m = len(sturm_seq)
    if sturm_seq[m - 1] == nan or sturm_seq[m - 1] == 0:
        sturm_seq.pop(m - 1)

    return sturm_seq

