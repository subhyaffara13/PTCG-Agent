
def _det_bird(M):
    r"""Compute the determinant of a matrix using Bird's algorithm.

    Bird's algorithm is a simple division-free algorithm for computing, which
    is of lower order than the Laplace's algorithm. It is described in [1]_.

    References
    ==========

    .. [1] Bird, R. S. (2011). A simple division-free algorithm for computing
           determinants. Inf. Process. Lett., 111(21), 1072-1074. doi:
           10.1016/j.ipl.2011.08.006
    """
    def mu(X):
        n = X.shape[0]
        zero = X.domain.zero

        total = zero
        diag_sums = [zero]
        for i in reversed(range(1, n)):
            total -= X[i][i]
            diag_sums.append(total)
        diag_sums = diag_sums[::-1]

        elems = [[zero] * i + [diag_sums[i]] + X_i[i + 1:] for i, X_i in
                 enumerate(X)]
        return DDM(elems, X.shape, X.domain)

    Mddm = M._rep.to_ddm()
    n = M.shape[0]
    if n == 0:
        return M.one
        # sympy/matrices/tests/test_matrices.py contains a test that
        # suggests that the determinant of a 0 x 0 matrix is one, by
        # convention.
    Fn1 = Mddm
    for _ in range(n - 1):
        Fn1 = mu(Fn1).matmul(Mddm)
    detA = Fn1[0][0]
    if n % 2 == 0:
        detA = -detA

    return Mddm.domain.to_sympy(detA)

