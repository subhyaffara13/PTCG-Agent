
def test_maxiter_worsening(solver, xp):
    if solver not in (gmres, lgmres, qmr):
        # these were skipped from the very beginning, see gh-9201; gh-14160
        pytest.skip("Solver breakdown case")
    # Check error does not grow (boundlessly) with increasing maxiter.
    # This can occur due to the solvers hitting close to breakdown,
    # which they should detect and halt as necessary.
    # cf. gh-9100
    if (solver is lgmres and
            platform.machine() not in ['x86_64' 'x86', 'aarch64', 'arm64']):
        # see gh-17839
        pytest.xfail(reason="fails on at least ppc64le, ppc64 and riscv64")

    # Singular matrix, rhs numerically not in range
    A = np.array([[-0.1112795288033378, 0, 0, 0.16127952880333685],
                  [0, -0.13627952880333782 + 6.283185307179586j, 0, 0],
                  [0, 0, -0.13627952880333782 - 6.283185307179586j, 0],
                  [0.1112795288033368, 0j, 0j, -0.16127952880333785]])
    v = np.ones(4)
    dtype = xpx.default_dtype(xp)
    A, v = (xp.asarray(arr, dtype=dtype) for arr in [A, v])
    best_error = np.inf

    # Unable to match the Fortran code tolerance levels with this example
    # Original tolerance values

    # slack_tol = 7 if platform.machine() == 'aarch64' else 5
    slack_tol = 9

    rtol = 1e-8
    for maxiter in range(1, 20):
        x, info = solver(A, v, maxiter=maxiter, rtol=rtol, atol=0.0)
        if info == 0:
            _assert_success(A=A, x=x, b=v, xp=xp, rtol=rtol)

        # Check with slack
        error = xp_vector_norm(A @ x - v)
        best_error = xp.min(best_error, error)
        assert error <= slack_tol * best_error

