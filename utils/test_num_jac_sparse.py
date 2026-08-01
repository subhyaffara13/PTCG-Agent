
def test_num_jac_sparse(structure_type):
    def fun(t, y):
        e = y[1:]**3 - y[:-1]**2
        z = np.zeros(y.shape[1])
        return np.vstack((z, 3 * e)) + np.vstack((2 * e, z))

    def structure(n):
        A = np.zeros((n, n), dtype=int)
        A[0, 0] = 1
        A[0, 1] = 1
        for i in range(1, n - 1):
            A[i, i - 1: i + 2] = 1
        A[-1, -1] = 1
        A[-1, -2] = 1

        return structure_type(A)

    np.random.seed(0)
    n = 20
    y = np.random.randn(n)
    A = structure(n)
    groups = group_columns(A)

    f = fun(0, y[:, None]).ravel()

    # Compare dense and sparse results, assuming that dense implementation
    # is correct (as it is straightforward).
    J_num_sparse, factor_sparse = num_jac(fun, 0, y.ravel(), f, 1e-8, None,
                                          sparsity=(A, groups))
    J_num_dense, factor_dense = num_jac(fun, 0, y.ravel(), f, 1e-8, None)
    assert_allclose(J_num_dense, J_num_sparse.toarray(),
                    rtol=1e-12, atol=1e-14)
    assert_allclose(factor_dense, factor_sparse, rtol=1e-12, atol=1e-14)

    # Take small factors to trigger their recomputing inside.
    factor = np.random.uniform(0, 1e-12, size=n)
    J_num_sparse, factor_sparse = num_jac(fun, 0, y.ravel(), f, 1e-8, factor,
                                          sparsity=(A, groups))
    J_num_dense, factor_dense = num_jac(fun, 0, y.ravel(), f, 1e-8, factor)

    assert_allclose(J_num_dense, J_num_sparse.toarray(),
                    rtol=1e-12, atol=1e-14)
    assert_allclose(factor_dense, factor_sparse, rtol=1e-12, atol=1e-14)

