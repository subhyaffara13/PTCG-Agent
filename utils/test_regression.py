
def test_regression():
    """Check the eigenvalue of the identity matrix is one.
    """
    # https://mail.python.org/pipermail/scipy-user/2010-October/026944.html
    n = 10
    X = np.ones((n, 1))
    A = np.identity(n)
    w, _ = lobpcg(A, X)
    assert_allclose(w, [1])

