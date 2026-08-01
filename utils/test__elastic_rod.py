
def test_ElasticRod(n):
    """Check eigh vs. lobpcg consistency for elastic rod model.
    """
    A, B = ElasticRod(n)
    m = 2
    rnd = np.random.RandomState(0)
    X = rnd.standard_normal((n, m))
    eigvals, _ = lobpcg(A, X, B=B, tol=1e-2, maxiter=50, largest=False)
    eigvals.sort()
    w, _ = eigh(A, b=B)
    w.sort()
    assert_almost_equal(w[:int(m/2)], eigvals[:int(m/2)], decimal=2)

