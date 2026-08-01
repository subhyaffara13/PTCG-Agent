
def sdm_particular_from_rref(A, ncols, pivots):
    """Get a particular solution from A which is in RREF"""
    P = {}
    for i, j in enumerate(pivots):
        Ain = A[i].get(ncols-1, None)
        if Ain is not None:
            P[j] = Ain / A[i][j]
    return P

