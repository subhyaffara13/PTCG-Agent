
def test_maxiter(case, xp, batch_A, batch_b):
    case = xp_case(case, xp, batch_A, batch_b, rng=38)
    if not case.convergence:
        pytest.skip("Solver - Breakdown case, see gh-8829")
    A = case.A
    rtol = 1e-12

    b = case.b
    x0 = 0 * b

    residuals = []

    def callback(x):
        if x.ndim == 0:
            residuals.append(xp_vector_norm(b - case.A * x))
        else:
            Ax = xp.squeeze(case.A @ x[..., xp.newaxis], axis=-1)
            residuals.append(xp_vector_norm(b - Ax, axis=-1))

    if case.solver == gmres:
        with pytest.warns(DeprecationWarning, match=CB_TYPE_FILTER):
            x, info = case.solver(A, b, x0=x0, rtol=rtol, maxiter=1, callback=callback)
    else:
        x, info = case.solver(A, b, x0=x0, rtol=rtol, maxiter=1, callback=callback)

    assert len(residuals) == 1
    assert info == 1

