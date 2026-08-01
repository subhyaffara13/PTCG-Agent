
def test_standard_nonsymmetric_no_convergence():
    rng = np.random.RandomState(1234)
    m = generate_matrix(30, complex_=True, rng=rng)
    tol, rtol, atol = _get_test_tolerance('d')
    try:
        w, v = eigs(m, 4, which='LM', v0=m[:, 0], maxiter=5, tol=tol)
        raise AssertionError("Spurious no-error exit")
    except ArpackNoConvergence as err:
        k = len(err.eigenvalues)
        if k <= 0:
            raise AssertionError("Spurious no-eigenvalues-found case") from err
        w, v = err.eigenvalues, err.eigenvectors
        for ww, vv in zip(w, v.T):
            assert_allclose(dot(m, vv), ww * vv, rtol=rtol, atol=atol)

