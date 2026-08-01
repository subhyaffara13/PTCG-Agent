
def correct_sign(deg_f, deg_g, s1, rdel, cdel):
    """
    Used in various subresultant prs algorithms.

    Evaluates the determinant, (a.k.a. subresultant) of a properly selected
    submatrix of s1, Sylvester's matrix of 1840, to get the correct sign
    and value of the leading coefficient of a given polynomial remainder.

    deg_f, deg_g are the degrees of the original polynomials p, q for which the
    matrix s1 = sylvester(p, q, x, 1) was constructed.

    rdel denotes the expected degree of the remainder; it is the number of
    rows to be deleted from each group of rows in s1 as described in the
    reference below.

    cdel denotes the expected degree minus the actual degree of the remainder;
    it is the number of columns to be deleted --- starting with the last column
    forming the square matrix --- from the matrix resulting after the row deletions.

    References
    ==========
    Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``Sturm Sequences
    and Modified Subresultant Polynomial Remainder Sequences.''
    Serdica Journal of Computing, Vol. 8, No 1, 29-46, 2014.

    """
    M = s1[:, :]   # copy of matrix s1

    # eliminate rdel rows from the first deg_g rows
    for i in range(M.rows - deg_f - 1, M.rows - deg_f - rdel - 1, -1):
        M.row_del(i)

    # eliminate rdel rows from the last deg_f rows
    for i in range(M.rows - 1, M.rows - rdel - 1, -1):
        M.row_del(i)

    # eliminate cdel columns
    for i in range(cdel):
        M.col_del(M.rows - 1)

    # define submatrix
    Md = M[:, 0: M.rows]

    return Md.det()

