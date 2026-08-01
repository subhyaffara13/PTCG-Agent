
def test_sakurai():
    """Check lobpcg and eighs accuracy for the Sakurai example
    already used in `benchmarks/benchmarks/sparse_linalg_lobpcg.py`.
    """
    n = 50
    tol = 100 * n * n * n* np.finfo(float).eps
    sakurai_obj = Sakurai(n, dtype='int')
    A = sakurai_obj
    m = 3
    ee = sakurai_obj.eigenvalues(3)
    rng = np.random.default_rng(0)
    X = rng.normal(size=(n, m))
    el, _ = lobpcg(A, X, tol=1e-9, maxiter=5000, largest=False)
    accuracy = max(abs(ee - el) / ee)
    assert_allclose(accuracy, 0., atol=tol)
    a_l = LinearOperator((n, n), matvec=A, matmat=A, dtype='float64')
    ea, _ = eigsh(a_l, k=m, which='SA', tol=1e-9, maxiter=15000,
                  v0 = rng.normal(size=(n, 1)))
    accuracy = max(abs(ee - ea) / ee)
    assert_allclose(accuracy, 0., atol=tol)

