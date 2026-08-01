
def test_sparse_hessian(method, sparse_type):
    # gh-8792 reported an error for minimization with `newton_cg` when `hess`
    # returns a sparse array. Check that results are the same whether `hess`
    # returns a dense or sparse array for optimization methods that accept
    # sparse Hessian matrices.

    def sparse_rosen_hess(x):
        return sparse_type(rosen_hess(x))

    x0 = [2., 2.]

    res_sparse = optimize.minimize(rosen, x0, method=method,
                                   jac=rosen_der, hess=sparse_rosen_hess)
    res_dense = optimize.minimize(rosen, x0, method=method,
                                  jac=rosen_der, hess=rosen_hess)

    assert_allclose(res_dense.fun, res_sparse.fun)
    assert_allclose(res_dense.x, res_sparse.x)
    assert res_dense.nfev == res_sparse.nfev
    assert res_dense.njev == res_sparse.njev
    assert res_dense.nhev == res_sparse.nhev

