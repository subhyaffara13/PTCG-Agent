
def modified_subresultants_pg(p, q, x):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the ``modified'' subresultant prs of p and q in Z[x] or Q[x];
    the coefficients of the polynomials in the sequence are
    ``modified'' subresultants. That is, they are  determinants of appropriately
    selected submatrices of sylvester2, Sylvester's matrix of 1853.

    To compute the coefficients, no determinant evaluation takes place. Instead,
    polynomial divisions in Q[x] are performed, using the function rem(p, q, x);
    the coefficients of the remainders computed this way become ``modified''
    subresultants with the help of the Pell-Gordon Theorem of 1917.

    If the ``modified'' subresultant prs is complete, and LC( p ) > 0, it coincides
    with the (generalized) Sturm sequence of the polynomials p, q.

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
    d0 =  degree(p,x)
    d1 =  degree(q,x)
    if d0 == 0 and d1 == 0:
        return [p, q]
    if d1 > d0:
        d0, d1 = d1, d0
        p, q = q, p
    if d0 > 0 and d1 == 0:
        return [p,q]

    # initialize
    k =  var('k')                               # index in summation formula
    u_list = []                                 # of elements (-1)**u_i
    subres_l = [p, q]                           # mod. subr. prs output list
    a0, a1 = p, q                               # the input polys
    del0 = d0 - d1                              # degree difference
    degdif = del0                               # save it
    rho_1 = LC(a0)                              # lead. coeff (a0)

    # Initialize Pell-Gordon variables
    rho_list_minus_1 =  sign( LC(a0, x))      # sign of LC(a0)
    rho1 =  LC(a1, x)                         # leading coeff of a1
    rho_list = [ sign(rho1)]                  # of signs
    p_list = [del0]                           # of degree differences
    u =  summation(k, (k, 1, p_list[0]))      # value of u
    u_list.append(u)                          # of u values
    v = sum(p_list)                           # v value

    # first remainder
    exp_deg = d1 - 1                          # expected degree of a2
    a2 = - rem(a0, a1, domain=QQ)             # first remainder
    rho2 =  LC(a2, x)                         # leading coeff of a2
    d2 =  degree(a2, x)                       # actual degree of a2
    deg_diff_new = exp_deg - d2               # expected - actual degree
    del1 = d1 - d2                            # degree difference

    # mul_fac is the factor by which a2 is multiplied to
    # get integer coefficients
    mul_fac_old = rho1**(del0 + del1 - deg_diff_new)

    # update Pell-Gordon variables
    p_list.append(1 + deg_diff_new)              # deg_diff_new is 0 for complete seq

    # apply Pell-Gordon formula (7) in second reference
    num = 1                                     # numerator of fraction
    for u in u_list:
        num *= (-1)**u
    num = num * (-1)**v

    # denominator depends on complete / incomplete seq
    if deg_diff_new == 0:                        # complete seq
        den = 1
        for k in range(len(rho_list)):
            den *= rho_list[k]**(p_list[k] + p_list[k + 1])
        den = den * rho_list_minus_1
    else:                                       # incomplete seq
        den = 1
        for k in range(len(rho_list)-1):
            den *= rho_list[k]**(p_list[k] + p_list[k + 1])
        den = den * rho_list_minus_1
        expo = (p_list[len(rho_list) - 1] + p_list[len(rho_list)] - deg_diff_new)
        den = den * rho_list[len(rho_list) - 1]**expo

    # the sign of the determinant depends on sg(num / den)
    if  sign(num / den) > 0:
        subres_l.append( simplify(rho_1**degdif*a2* Abs(mul_fac_old) ) )
    else:
        subres_l.append(- simplify(rho_1**degdif*a2* Abs(mul_fac_old) ) )

    # update Pell-Gordon variables
    k = var('k')
    rho_list.append( sign(rho2))
    u =  summation(k, (k, 1, p_list[len(p_list) - 1]))
    u_list.append(u)
    v = sum(p_list)
    deg_diff_old=deg_diff_new

    # main loop
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

        mul_fac_new = rho2**(expo_new) * rho1**(expo_old) * mul_fac_old

        # update variables
        deg_diff_old, mul_fac_old = deg_diff_new, mul_fac_new
        rho1, rho2 = rho2, rho3

        # update Pell-Gordon variables
        p_list.append(1 + deg_diff_new)       # deg_diff_new is 0 for complete seq

        # apply Pell-Gordon formula (7) in second reference
        num = 1                              # numerator
        for u in u_list:
            num *= (-1)**u
        num = num * (-1)**v

        # denominator depends on complete / incomplete seq
        if deg_diff_new == 0:                 # complete seq
            den = 1
            for k in range(len(rho_list)):
                den *= rho_list[k]**(p_list[k] + p_list[k + 1])
            den = den * rho_list_minus_1
        else:                                # incomplete seq
            den = 1
            for k in range(len(rho_list)-1):
                den *= rho_list[k]**(p_list[k] + p_list[k + 1])
            den = den * rho_list_minus_1
            expo = (p_list[len(rho_list) - 1] + p_list[len(rho_list)] - deg_diff_new)
            den = den * rho_list[len(rho_list) - 1]**expo

        # the sign of the determinant depends on sg(num / den)
        if  sign(num / den) > 0:
            subres_l.append( simplify(rho_1**degdif*a2* Abs(mul_fac_old) ) )
        else:
            subres_l.append(- simplify(rho_1**degdif*a2* Abs(mul_fac_old) ) )

        # update Pell-Gordon variables
        k = var('k')
        rho_list.append( sign(rho2))
        u =  summation(k, (k, 1, p_list[len(p_list) - 1]))
        u_list.append(u)
        v = sum(p_list)

    # gcd is of degree > 0 ?
    m = len(subres_l)
    if subres_l[m - 1] == nan or subres_l[m - 1] == 0:
        subres_l.pop(m - 1)

    # LC( p ) < 0
    m = len(subres_l)   # list may be shorter now due to deg(gcd ) > 0
    if LC( p ) < 0:
        aux_seq = [subres_l[0], subres_l[1]]
        for i in range(2, m):
            aux_seq.append(simplify(subres_l[i] * (-1) ))
        subres_l = aux_seq

    return  subres_l

