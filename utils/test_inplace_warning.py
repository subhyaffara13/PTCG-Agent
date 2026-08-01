
def test_inplace_warning():
    """Check lobpcg gives a warning in '_b_orthonormalize'
    that in-place orthogonalization is impossible due to dtype mismatch.
    """
    rnd = np.random.RandomState(0)
    n = 6
    m = 1
    vals = -np.arange(1, n + 1)
    A = dia_array(([vals], [0]), shape=(n, n))
    A = A.astype(np.cdouble)
    X = rnd.standard_normal((n, m))
    with pytest.warns(UserWarning, match="Inplace update"):
        eigvals, _ = lobpcg(A, X, maxiter=2, verbosityLevel=1)

