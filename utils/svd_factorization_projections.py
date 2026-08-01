
def svd_factorization_projections(A, m, n, orth_tol, max_refin, tol):
    """Return linear operators for matrix A using ``SVDFactorization`` approach.
    """
    # SVD Factorization
    U, s, Vt = scipy.linalg.svd(A, full_matrices=False)

    # Remove dimensions related with very small singular values
    U = U[:, s > tol]
    Vt = Vt[s > tol, :]
    s = s[s > tol]

    # z = x - A.T inv(A A.T) A x
    def null_space(x):
        # v = U 1/s V.T x = inv(A A.T) A x
        aux1 = Vt.dot(x)
        aux2 = 1/s*aux1
        v = U.dot(aux2)
        z = x - A.T.dot(v)

        # Iterative refinement to improve roundoff
        # errors described in [2]_, algorithm 5.1.
        k = 0
        while orthogonality(A, z) > orth_tol:
            if k >= max_refin:
                break
            # v = U 1/s V.T x = inv(A A.T) A x
            aux1 = Vt.dot(z)
            aux2 = 1/s*aux1
            v = U.dot(aux2)
            # z_next = z - A.T v
            z = z - A.T.dot(v)
            k += 1

        return z

    # z = inv(A A.T) A x
    def least_squares(x):
        # z = U 1/s V.T x = inv(A A.T) A x
        aux1 = Vt.dot(x)
        aux2 = 1/s*aux1
        z = U.dot(aux2)
        return z

    # z = A.T inv(A A.T) x
    def row_space(x):
        # z = V 1/s U.T x
        aux1 = U.T.dot(x)
        aux2 = 1/s*aux1
        z = Vt.T.dot(aux2)
        return z

    return null_space, least_squares, row_space

