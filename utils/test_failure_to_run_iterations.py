
def test_failure_to_run_iterations():
    """Check that the code exits gracefully without breaking. Issue #10974.
    The code may or not issue a warning, filtered out. Issue #15935, #17954.
    """
    rnd = np.random.RandomState(0)
    X = rnd.standard_normal((100, 10))
    A = X @ X.T
    Q = rnd.standard_normal((X.shape[0], 4))
    eigenvalues, _ = lobpcg(A, Q, maxiter=40, tol=1e-12)
    assert np.max(eigenvalues) > 0

