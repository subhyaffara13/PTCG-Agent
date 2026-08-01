
def test_nonhermitian_warning(capsys):
    """Check the warning of a Ritz matrix being not Hermitian
    by feeding a non-Hermitian input matrix.
    Also check stdout since verbosityLevel=1 and lack of stderr.
    """
    n = 10
    X = np.arange(n * 2).reshape(n, 2).astype(np.float32)
    A = np.arange(n * n).reshape(n, n).astype(np.float32)
    with pytest.warns(UserWarning, match="Matrix gramA"):
        _, _ = lobpcg(A, X, verbosityLevel=1, maxiter=0)
    out, err = capsys.readouterr()  # Capture output
    assert out.startswith("Solving standard eigenvalue")  # Test stdout
    assert err == ''  # Test empty stderr
    # Make the matrix symmetric and the UserWarning disappears.
    A += A.T
    _, _ = lobpcg(A, X, verbosityLevel=1, maxiter=0)
    out, err = capsys.readouterr()  # Capture output
    assert out.startswith("Solving standard eigenvalue")  # Test stdout
    assert err == ''  # Test empty stderr

