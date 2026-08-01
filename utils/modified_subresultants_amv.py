
def modified_subresultants_amv(p, q, x):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the modified subresultant prs of p and q in Z[x] or Q[x],
    from the subresultant prs of p and q.
    The coefficients of the polynomials in the two sequences differ only
    in sign and the factor LC(p)**( deg(p)- deg(q)) as stated in
    Theorem 2 of the reference.

    The coefficients of the polynomials in the output sequence are
    modified subresultants. That is, they are  determinants of appropriately
    selected submatrices of sylvester2, Sylvester's matrix of 1853.

    If the modified subresultant prs is complete, and LC( p ) > 0, it coincides
    with the (generalized) Sturm's sequence of the polynomials p, q.

    References
    ==========
    1. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: "On the Remainders
    Obtained in Finding the Greatest Common Divisor of Two Polynomials."
    Serdica Journal of Computing, Serdica Journal of Computing, 9(2) (2015), 123-138.

    """
    # compute the subresultant prs
    lst = subresultants_amv(p,q,x)     ## any other method would do

    # defensive
    if lst == [] or len(lst) == 2:
        return lst

    # the coefficients in lst are subresultants and, hence, smaller than those
    # of the corresponding modified subresultants by the factor
    # LC(lst[0])**( deg(lst[0]) - deg(lst[1])); see Theorem 2.
    lcf = LC(lst[0])**( degree(lst[0], x) - degree(lst[1], x) )

    # Initialize the modified subresultant prs list
    subr_seq = [lst[0], lst[1]]

    # compute the degree sequences m_i and j_i of Theorem 2
    deg_seq = [degree(Poly(poly, x), x) for poly in lst]
    deg = deg_seq[0]
    deg_seq_s = deg_seq[1:-1]
    m_seq = [m-1 for m in deg_seq_s]
    j_seq = [deg - m for m in m_seq]

    # compute the AMV factors of Theorem 2
    fact = [(-1)**( j*(j-1)/S(2) ) for j in j_seq]

    # shortened list without the first two polys
    lst_s = lst[2:]

    # poly lst_s[k] is multiplied times fact[k] and times lcf
    # and appended to the subresultant prs list
    m = len(fact)
    for k in range(m):
        if sign(fact[k]) == -1:
            subr_seq.append( simplify(-lst_s[k] * lcf) )
        else:
            subr_seq.append( simplify(lst_s[k] * lcf) )

    return subr_seq

