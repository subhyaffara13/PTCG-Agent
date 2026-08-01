
def test_eigsh_consistency(n, atol):
    """Check eigsh vs. lobpcg consistency.
    """
    vals = np.arange(1, n+1, dtype=np.float64)
    A = dia_array((vals, 0), shape=(n, n))
    rnd = np.random.RandomState(0)
    X = rnd.standard_normal((n, 2))
    lvals, lvecs = lobpcg(A, X, largest=True, maxiter=100)
    vals, _ = eigsh(A, k=2)

    _check_eigen(A, lvals, lvecs, atol=atol, rtol=0)
    assert_allclose(np.sort(vals), np.sort(lvals), atol=1e-14)

