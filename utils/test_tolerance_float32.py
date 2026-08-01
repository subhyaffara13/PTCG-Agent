
def test_tolerance_float32():
    """Check lobpcg for attainable tolerance in float32.
    """
    rnd = np.random.RandomState(0)
    n = 50
    m = 3
    vals = -np.arange(1, n + 1)
    A = dia_array(([vals], [0]), shape=(n, n))
    A = A.astype(np.float32)
    X = rnd.standard_normal((n, m))
    X = X.astype(np.float32)
    eigvals, _ = lobpcg(A, X, tol=1.25e-5, maxiter=50, verbosityLevel=0)
    assert_allclose(eigvals, -np.arange(1, 1 + m), atol=2e-5, rtol=1e-5)

