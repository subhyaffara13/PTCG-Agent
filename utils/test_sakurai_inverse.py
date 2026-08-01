
def test_sakurai_inverse(n):
    """Check lobpcg and eighs accuracy for the sakurai_inverse example
    already used in `benchmarks/benchmarks/sparse_linalg_lobpcg.py`.
    """
    def a(x):
        return cho_solve_banded((c, False), x)
    tol = 100 * n * n * n* np.finfo(float).eps
    sakurai_obj = Sakurai(n)
    A = sakurai_obj.tobanded().astype(np.float64)
    m = 3
    ee = sakurai_obj.eigenvalues(3)
    rng = np.random.default_rng(0)
    X = rng.normal(size=(n, m))
    c = cholesky_banded(A)
    el, _ = lobpcg(a, X, tol=1e-9, maxiter=8)
    accuracy = max(abs(ee - 1. / el) / ee)
    assert_allclose(accuracy, 0., atol=tol)
    a_l = LinearOperator((n, n), matvec=a, matmat=a, dtype='float64')
    ea, _ = eigsh(a_l, k=m, which='LA', tol=1e-9, maxiter=8,
                  v0 = rng.normal(size=(n, 1)))
    accuracy = max(abs(ee - np.sort(1. / ea)) / ee)
    assert_allclose(accuracy, 0., atol=tol)

