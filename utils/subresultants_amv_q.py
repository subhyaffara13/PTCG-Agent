
def subresultants_amv_q(p, q, x):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the subresultant prs of p and q in Q[x];
    the coefficients of the polynomials in the sequence are
    subresultants. That is, they are  determinants of appropriately
    selected submatrices of sylvester1, Sylvester's matrix of 1840.

    To compute the coefficients, no determinant evaluation takes place.
    Instead, polynomial divisions in Q[x] are performed, using the
    function rem(p, q, x);  the coefficients of the remainders
    computed this way become subresultants with the help of the
    Akritas-Malaschonok-Vigklas Theorem of 2015.

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
        return [p, q]

    # initialize
    i, s = 0, 0                              # counters for remainders & odd elements
    p_odd_index_sum = 0                      # contains the sum of p_1, p_3, etc
    subres_l = [p, q]                        # subresultant prs output list
    a0, a1 = p, q                            # the input polys
    sigma1 =  LC(a1, x)                      # leading coeff of a1
    p0 = d0 - d1                             # degree difference
    if p0 % 2 == 1:
        s += 1
    phi = floor( (s + 1) / 2 )
    mul_fac = 1
    d2 = d1

    # main loop
    while d2 > 0:
        i += 1
        a2 = rem(a0, a1, domain= QQ)          # new remainder
        if i == 1:
            sigma2 =  LC(a2, x)
        else:
            sigma3 =  LC(a2, x)
            sigma1, sigma2 = sigma2, sigma3
        d2 =  degree(a2, x)
        p1 = d1 - d2
        psi = i + phi + p_odd_index_sum

        # new mul_fac
        mul_fac = sigma1**(p0 + 1) * mul_fac

        ## compute the sign of the first fraction in formula (9) of the paper
        # numerator
        num = (-1)**psi
        # denominator
        den = sign(mul_fac)

        # the sign of the determinant depends on sign( num / den ) != 0
        if  sign(num / den) > 0:
            subres_l.append( simplify(expand(a2* Abs(mul_fac))))
        else:
            subres_l.append(- simplify(expand(a2* Abs(mul_fac))))

        ## bring into mul_fac the missing power of sigma if there was a degree gap
        if p1 - 1 > 0:
            mul_fac = mul_fac * sigma1**(p1 - 1)

       # update AMV variables
        a0, a1, d0, d1 = a1, a2, d1, d2
        p0 = p1
        if p0 % 2 ==1:
            s += 1
        phi = floor( (s + 1) / 2 )
        if i%2 == 1:
            p_odd_index_sum += p0             # p_i has odd index

    # gcd is of degree > 0 ?
    m = len(subres_l)
    if subres_l[m - 1] == nan or subres_l[m - 1] == 0:
        subres_l.pop(m - 1)

    return  subres_l

