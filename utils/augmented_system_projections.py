
def augmented_system_projections(A, m, n, orth_tol, max_refin, tol):
    """Return linear operators for matrix A - ``AugmentedSystem``."""
    # Form augmented system
    K = block_array([[eye_array(n), A.T], [A, None]], format="csc")
    # LU factorization
    # TODO: Use a symmetric indefinite factorization
    #       to solve the system twice as fast (because
    #       of the symmetry).
    try:
        solve = scipy.sparse.linalg.factorized(K)
    except RuntimeError:
        warn("Singular Jacobian matrix. Using dense SVD decomposition to "
             "perform the factorizations.",
             stacklevel=3)
        return svd_factorization_projections(A.toarray(),
                                             m, n, orth_tol,
                                             max_refin, tol)

    # z = x - A.T inv(A A.T) A x
    # is computed solving the extended system:
    # [I A.T] * [ z ] = [x]
    # [A  O ]   [aux]   [0]
    def null_space(x):
        # v = [x]
        #     [0]
        v = np.hstack([x, np.zeros(m)])
        # lu_sol = [ z ]
        #          [aux]
        lu_sol = solve(v)
        z = lu_sol[:n]

        # Iterative refinement to improve roundoff
        # errors described in [2]_, algorithm 5.2.
        k = 0
        while orthogonality(A, z) > orth_tol:
            if k >= max_refin:
                break
            # new_v = [x] - [I A.T] * [ z ]
            #         [0]   [A  O ]   [aux]
            new_v = v - K.dot(lu_sol)
            # [I A.T] * [delta  z ] = new_v
            # [A  O ]   [delta aux]
            lu_update = solve(new_v)
            #  [ z ] += [delta  z ]
            #  [aux]    [delta aux]
            lu_sol += lu_update
            z = lu_sol[:n]
            k += 1

        # return z = x - A.T inv(A A.T) A x
        return z

    # z = inv(A A.T) A x
    # is computed solving the extended system:
    # [I A.T] * [aux] = [x]
    # [A  O ]   [ z ]   [0]
    def least_squares(x):
        # v = [x]
        #     [0]
        v = np.hstack([x, np.zeros(m)])
        # lu_sol = [aux]
        #          [ z ]
        lu_sol = solve(v)
        # return z = inv(A A.T) A x
        return lu_sol[n:m+n]

    # z = A.T inv(A A.T) x
    # is computed solving the extended system:
    # [I A.T] * [ z ] = [0]
    # [A  O ]   [aux]   [x]
    def row_space(x):
        # v = [0]
        #     [x]
        v = np.hstack([np.zeros(n), x])
        # lu_sol = [ z ]
        #          [aux]
        lu_sol = solve(v)
        # return z = A.T inv(A A.T) x
        return lu_sol[:n]

    return null_space, least_squares, row_space

