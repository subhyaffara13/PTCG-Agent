
def _choose_2x2_inversion_formula(A, B, C, D):
    """
    Assuming [[A, B], [C, D]] would form a valid square block matrix, find
    which of the classical 2x2 block matrix inversion formulas would be
    best suited.

    Returns 'A', 'B', 'C', 'D' to represent the algorithm involving inversion
    of the given argument or None if the matrix cannot be inverted using
    any of those formulas.
    """
    # Try to find a known invertible matrix.  Note that the Schur complement
    # is currently not being considered for this
    A_inv = ask(Q.invertible(A))
    if A_inv == True:
        return 'A'
    B_inv = ask(Q.invertible(B))
    if B_inv == True:
        return 'B'
    C_inv = ask(Q.invertible(C))
    if C_inv == True:
        return 'C'
    D_inv = ask(Q.invertible(D))
    if D_inv == True:
        return 'D'
    # Otherwise try to find a matrix that isn't known to be non-invertible
    if A_inv != False:
        return 'A'
    if B_inv != False:
        return 'B'
    if C_inv != False:
        return 'C'
    if D_inv != False:
        return 'D'
    return None

