
def _is_conditionally_positive_definite(kernel, m):
    # Tests whether the kernel is conditionally positive definite of order m.
    # See chapter 7 of Fasshauer's "Meshfree Approximation Methods with
    # MATLAB".
    nx = 10
    ntests = 100
    for ndim in [1, 2, 3, 4, 5]:
        # Generate sample points with a Halton sequence to avoid samples that
        # are too close to each other, which can make the matrix singular.
        seq = Halton(ndim, scramble=False, seed=np.random.RandomState())
        for _ in range(ntests):
            x = 2*seq.random(nx) - 1
            A = _rbfinterp_pythran._kernel_matrix(x, kernel)
            P = _vandermonde(x, m - 1)
            Q, R = np.linalg.qr(P, mode='complete')
            # Q2 forms a basis spanning the space where P.T.dot(x) = 0. Project
            # A onto this space, and then see if it is positive definite using
            # the Cholesky decomposition. If not, then the kernel is not c.p.d.
            # of order m.
            Q2 = Q[:, P.shape[1]:]
            B = Q2.T.dot(A).dot(Q2)
            try:
                np.linalg.cholesky(B)
            except np.linalg.LinAlgError:
                return False

    return True

