
def euclid_q(p, q, x):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the Euclidean sequence of p and q in Q[x].
    Polynomial divisions in Q[x] are performed, using the function rem(p, q, x).

    The coefficients of the polynomials in the Euclidean sequence can be uniquely
    determined from the corresponding coefficients of the polynomials found
    either in:

        (a) the ``modified'' subresultant polynomial remainder sequence,
    (references 1, 2)

    or in

        (b) the subresultant polynomial remainder sequence (references 3).

    References
    ==========
    1. Pell A. J., R. L. Gordon. The Modified Remainders Obtained in Finding
    the Highest Common Factor of Two Polynomials. Annals of MatheMatics,
    Second Series, 18 (1917), No. 4, 188-193.

    2. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``Sturm Sequences
    and Modified Subresultant Polynomial Remainder Sequences.''
    Serdica Journal of Computing, Vol. 8, No 1, 29-46, 2014.

    3. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``A Basic Result
    on the Theory of Subresultants.'' Serdica Journal of Computing 10 (2016), No.1, 31-48.

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
    a0, a1 = p, q                           # the input polys
    euclid_seq = [a0, a1]                   # the output list
    a2 = rem(a0, a1, domain=QQ)             # first remainder
    d2 =  degree(a2, x)                     # degree of a2
    euclid_seq.append( a2 )

    # main loop
    while d2 > 0:
        a0, a1, d0, d1 = a1, a2, d1, d2      # update polys and degrees
        a2 = rem(a0, a1, domain=QQ)          # new remainder
        d2 =  degree(a2, x)                  # actual degree of a2
        euclid_seq.append( a2 )

    if flag:          # change the sign of the sequence
        euclid_seq = [-i for i in euclid_seq]

    # gcd is of degree > 0 ?
    m = len(euclid_seq)
    if euclid_seq[m - 1] == nan or euclid_seq[m - 1] == 0:
        euclid_seq.pop(m - 1)

    return euclid_seq

