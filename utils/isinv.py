
def isinv(A, B, tol=None):
    '''
    This procedure tests whether A = B^{-1} up to the tolerance TOL.
    '''

    # Sizes
    n = np.size(A, 0)

    # Preconditions
    if DEBUGGING:
        assert np.size(A, 0) == np.size(A, 1)
        assert np.size(B, 0) == np.size(B, 1)
        assert np.size(A, 0) == np.size(B, 0)
        if present(tol):
            assert tol >= 0

    #====================#
    # Calculation starts #
    #====================#

    tol = tol if present(tol) else np.minimum(1e-3, 1e2 * EPS * np.maximum(np.size(A, 0), np.size(A, 1)))
    tol = np.max([tol, tol * np.max(abs(A)), tol * np.max(abs(B))])
    is_inv = ((abs(matprod(A, B)) - np.eye(n)) <= tol).all() or ((abs(matprod(B, A) - np.eye(n))) <= tol).all()

    #===================#
    #  Calculation ends #
    #===================#
    return is_inv

