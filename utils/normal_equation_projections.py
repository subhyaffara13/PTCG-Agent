
def normal_equation_projections(A, m, n, orth_tol, max_refin, tol):
    """Return linear operators for matrix A using ``NormalEquation`` approach.
    """
    # Cholesky factorization
    # TODO: revert this once the warning bug fix in sksparse is merged/released
    # Add suppression of spurious warning bug from sksparse with csc_array gh-22089
    # factor = cholesky_AAt(A)
    with catch_warnings(action='ignore', category=CholmodTypeConversionWarning):
        factor = cholesky_AAt(A)

    # z = x - A.T inv(A A.T) A x
    def null_space(x):
        v = factor(A.dot(x))
        z = x - A.T.dot(v)

        # Iterative refinement to improve roundoff
        # errors described in [2]_, algorithm 5.1.
        k = 0
        while orthogonality(A, z) > orth_tol:
            if k >= max_refin:
                break
            # z_next = z - A.T inv(A A.T) A z
            v = factor(A.dot(z))
            z = z - A.T.dot(v)
            k += 1

        return z

    # z = inv(A A.T) A x
    def least_squares(x):
        return factor(A.dot(x))

    # z = A.T inv(A A.T) x
    def row_space(x):
        return A.T.dot(factor(x))

    return null_space, least_squares, row_space

