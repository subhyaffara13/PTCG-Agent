
def qr_factorization_projections(A, m, n, orth_tol, max_refin, tol):
    """Return linear operators for matrix A using ``QRFactorization`` approach.
    """
    # QRFactorization
    Q, R, P = scipy.linalg.qr(A.T, pivoting=True, mode='economic')

    if np.linalg.norm(R[-1, :], np.inf) < tol:
        warn('Singular Jacobian matrix. Using SVD decomposition to ' +
             'perform the factorizations.',
             stacklevel=3)
        return svd_factorization_projections(A, m, n,
                                             orth_tol,
                                             max_refin,
                                             tol)

    # z = x - A.T inv(A A.T) A x
    def null_space(x):
        # v = P inv(R) Q.T x
        aux1 = Q.T.dot(x)
        aux2 = scipy.linalg.solve_triangular(R, aux1, lower=False)
        v = np.zeros(m)
        v[P] = aux2
        z = x - A.T.dot(v)

        # Iterative refinement to improve roundoff
        # errors described in [2]_, algorithm 5.1.
        k = 0
        while orthogonality(A, z) > orth_tol:
            if k >= max_refin:
                break
            # v = P inv(R) Q.T x
            aux1 = Q.T.dot(z)
            aux2 = scipy.linalg.solve_triangular(R, aux1, lower=False)
            v[P] = aux2
            # z_next = z - A.T v
            z = z - A.T.dot(v)
            k += 1

        return z

    # z = inv(A A.T) A x
    def least_squares(x):
        # z = P inv(R) Q.T x
        aux1 = Q.T.dot(x)
        aux2 = scipy.linalg.solve_triangular(R, aux1, lower=False)
        z = np.zeros(m)
        z[P] = aux2
        return z

    # z = A.T inv(A A.T) x
    def row_space(x):
        # z = Q inv(R.T) P.T x
        aux1 = x[P]
        aux2 = scipy.linalg.solve_triangular(R, aux1,
                                             lower=False,
                                             trans='T')
        z = Q.dot(aux2)
        return z

    return null_space, least_squares, row_space

