
def euclid_pg(p, q, x):
    """
    p, q are polynomials in Z[x] or Q[x]. It is assumed
    that degree(p, x) >= degree(q, x).

    Computes the Euclidean sequence of p and q in Z[x] or Q[x].

    If the Euclidean sequence is complete the coefficients of the polynomials
    in the sequence are subresultants. That is, they are  determinants of
    appropriately selected submatrices of sylvester1, Sylvester's matrix of 1840.
    In this case the Euclidean sequence coincides with the subresultant prs
    of the polynomials p, q.

    If the Euclidean sequence is incomplete the signs of the coefficients of the
    polynomials in the sequence may differ from the signs of the coefficients of
    the corresponding polynomials in the subresultant prs; however, the absolute
    values are the same.

    To compute the Euclidean sequence, no determinant evaluation takes place.
    We first compute the (generalized) Sturm sequence  of p and q using
    sturm_pg(p, q, x, 1), in which case the coefficients are (in absolute value)
    equal to subresultants. Then we change the signs of the remainders in the
    Sturm sequence according to the pattern "-, -, +, +, -, -, +, +,..." ;
    see Lemma 1 in the 1st reference or Theorem 3 in the 2nd reference as well as
    the function sturm_pg(p, q, x).

    References
    ==========
    1. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``A Basic Result
    on the Theory of Subresultants.'' Serdica Journal of Computing 10 (2016), No.1, 31-48.

    2. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``On the Remainders
    Obtained in Finding the Greatest Common Divisor of Two Polynomials.'' Serdica
    Journal of Computing 9(2) (2015), 123-138.

    3. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``Subresultant Polynomial
    Remainder Sequences Obtained by Polynomial Divisions in Q[x] or in Z[x].''
    Serdica Journal of Computing 10 (2016), No.3-4, 197-217.
    """
    # compute the sturmian sequence using the Pell-Gordon (or AMV) theorem
    # with the coefficients in the prs being (in absolute value) subresultants
    prs = sturm_pg(p, q, x, 1)  ## any other method would do

    # defensive
    if prs == [] or len(prs) == 2:
        return prs

    # the signs of the first two polys in the sequence stay the same
    euclid_seq = [prs[0], prs[1]]

    # change the signs according to "-, -, +, +, -, -, +, +,..."
    flag = 0
    m = len(prs)
    i = 2
    while i <= m-1:
        if  flag == 0:
            euclid_seq.append(- prs[i] )
            i = i + 1
            if i == m:
                break
            euclid_seq.append(- prs[i] )
            i = i + 1
            flag = 1
        elif flag == 1:
            euclid_seq.append(prs[i] )
            i = i + 1
            if i == m:
                break
            euclid_seq.append(prs[i] )
            i = i + 1
            flag = 0

    return euclid_seq

