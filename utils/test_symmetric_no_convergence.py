
def test_symmetric_no_convergence():
    rng = np.random.RandomState(1234)
    m = generate_matrix(30, hermitian=True, pos_definite=True, rng=rng)
    tol, rtol, atol = _get_test_tolerance('d')
    try:
        w, v = eigsh(m, 4, which='LM', v0=m[:, 0], maxiter=5, tol=tol, ncv=9)
        raise AssertionError("Spurious no-error exit")
    except ArpackNoConvergence as err:
        k = len(err.eigenvalues)
        if k <= 0:
            raise AssertionError("Spurious no-eigenvalues-found case") from err
        w, v = err.eigenvalues, err.eigenvectors
        assert_allclose(dot(m, v), w * v, rtol=rtol, atol=atol)

