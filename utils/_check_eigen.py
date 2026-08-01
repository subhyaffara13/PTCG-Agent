
def _check_eigen(M, w, V, rtol=1e-8, atol=1e-14):
    """Check if the eigenvalue residual is small.
    """
    mult_wV = np.multiply(w, V)
    dot_MV = M.dot(V)
    assert_allclose(mult_wV, dot_MV, rtol=rtol, atol=atol)

