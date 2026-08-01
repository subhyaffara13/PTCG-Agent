
def test_zero_rhs(solver, xp, batch_A, batch_b):
    rng = np.random.default_rng(1684414984100503)
    dtype = xpx.default_dtype(xp) 
    A = xp.asarray(rng.random(size=(*batch_A, 10, 10)), dtype=dtype)
    A = A @ A.mT + 10 * xp.eye(10)

    b = xp.zeros((*batch_b, 10), dtype=dtype)
    tols = np.r_[np.logspace(-10, 2, 7)]

    expected = xp.broadcast_to(b, (*np.broadcast_shapes(batch_A, batch_b), 10))
    for tol in tols:
        tol = float(tol)
        x, info = solver(A, b, rtol=tol)
        assert info == 0
        xp_assert_close(x, expected, atol=1e-15)

        x, info = solver(A, b, rtol=tol, x0=xp.ones((*batch_b, 10)))
        assert info == 0
        xp_assert_close(x, expected, atol=tol)

        if solver is not minres:
            x, info = solver(A, b, rtol=tol, atol=0.0, x0=xp.ones((*batch_b, 10)))
            if info == 0:
                xp_assert_close(x, expected)

            x, info = solver(A, b, rtol=tol, atol=tol)
            assert info == 0
            xp_assert_close(x, expected, atol=1e-300)

            x, info = solver(A, b, rtol=tol, atol=0.0)
            assert info == 0
            xp_assert_close(x, expected, atol=1e-300)

