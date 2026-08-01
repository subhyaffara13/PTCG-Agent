
def _berkowitz_toeplitz_matrix(M):
    """Return (A,T) where T the Toeplitz matrix used in the Berkowitz algorithm
    corresponding to ``M`` and A is the first principal submatrix.
    """

    # the 0 x 0 case is trivial
    if M.rows == 0 and M.cols == 0:
        return M._new(1,1, [M.one])

    #
    # Partition M = [ a_11  R ]
    #                  [ C     A ]
    #

    a, R = M[0,0],   M[0, 1:]
    C, A = M[1:, 0], M[1:,1:]

    #
    # The Toeplitz matrix looks like
    #
    #  [ 1                                     ]
    #  [ -a         1                          ]
    #  [ -RC       -a        1                 ]
    #  [ -RAC     -RC       -a       1         ]
    #  [ -RA**2C -RAC      -RC      -a       1 ]
    #  etc.

    # Compute the diagonal entries.
    # Because multiplying matrix times vector is so much
    # more efficient than matrix times matrix, recursively
    # compute -R * A**n * C.
    diags = [C]
    for i in range(M.rows - 2):
        diags.append(A.multiply(diags[i], dotprodsimp=None))
    diags = [(-R).multiply(d, dotprodsimp=None)[0, 0] for d in diags]
    diags = [M.one, -a] + diags

    def entry(i,j):
        if j > i:
            return M.zero
        return diags[i - j]

    toeplitz = M._new(M.cols + 1, M.rows, entry)
    return (A, toeplitz)

