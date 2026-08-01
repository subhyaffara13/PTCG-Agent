
def isorth(A, tol=None):
    '''
    This function tests whether the matrix A has orthonormal columns up to the tolerance TOL.
    '''

    # Preconditions
    if DEBUGGING:
        if present(tol):
            assert tol >= 0

    #====================#
    # Calculation starts #
    #====================#

    num_vars = np.size(A, 1)

    if num_vars > np.size(A, 0):
        is_orth = False
    elif (np.isnan(primasum(abs(A)))):
        is_orth = False
    else:
        if present(tol):
            is_orth = (abs(matprod(A.T, A) - np.eye(num_vars)) <= np.maximum(tol, tol * np.max(abs(A)))).all()
        else:
            is_orth = (abs(matprod(A.T, A) - np.eye(num_vars)) <= 0).all()

    #====================#
    #  Calculation ends  #
    #====================#
    return is_orth

