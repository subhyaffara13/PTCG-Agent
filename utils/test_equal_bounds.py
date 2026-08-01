
def test_equal_bounds(method, kwds, bound_type, constraints, callback):
    """
    Tests that minimizers still work if (bounds.lb == bounds.ub).any()
    gh12502 - Divide by zero in Jacobian numerical differentiation when
    equality bounds constraints are used
    """
    # GH-15051; slightly more skips than necessary; hopefully fixed by GH-14882
    if (platform.machine() == 'aarch64' and method == "TNC"
            and kwds["jac"] is False and callback is not None):
        pytest.skip('Tolerance violation on aarch')

    lb, ub = eb_data["lb"], eb_data["ub"]
    x0, i_eb = eb_data["x0"], eb_data["i_eb"]

    test_constraints, reference_constraints = constraints
    if test_constraints and not method == 'SLSQP':
        pytest.skip('Only SLSQP supports nonlinear constraints')

    if method in ['SLSQP', 'TNC'] and callable(callback):
        sig = inspect.signature(callback)
        if 'intermediate_result' in set(sig.parameters):
            pytest.skip("SLSQP, TNC don't support intermediate_result")

    # reference constraints always have analytical jacobian
    # if test constraints are not the same, we'll need finite differences
    fd_needed = (test_constraints != reference_constraints)

    bounds = bound_type(lb, ub)  # old- or new-style

    kwds.update({"x0": x0, "method": method, "bounds": bounds,
                 "constraints": test_constraints, "callback": callback})
    res = optimize.minimize(**kwds)

    expected = optimize.minimize(optimize.rosen, x0, method=method,
                                 jac=optimize.rosen_der, bounds=bounds,
                                 constraints=reference_constraints)

    # compare the output of a solution with FD vs that of an analytic grad
    assert res.success
    assert_allclose(res.fun, expected.fun, rtol=5.0e-6)
    assert_allclose(res.x, expected.x, rtol=5e-4)

    if fd_needed or kwds['jac'] is False:
        expected.jac[i_eb] = np.nan
    assert res.jac.shape[0] == 4
    assert_allclose(res.jac[i_eb], expected.jac[i_eb], rtol=1e-6)

    if not (kwds['jac'] or test_constraints or isinstance(bounds, Bounds)):
        # compare the output to an equivalent FD minimization that doesn't
        # need factorization
        def fun(x):
            new_x = np.array([np.nan, 2, np.nan, -1])
            new_x[[0, 2]] = x
            return optimize.rosen(new_x)

        fd_res = optimize.minimize(fun,
                                   x0[[0, 2]],
                                   method=method,
                                   bounds=bounds[::2])
        assert_allclose(res.fun, fd_res.fun)
        # TODO this test should really be equivalent to factorized version
        # above, down to res.nfev. However, testing found that when TNC is
        # called with or without a callback the output is different. The two
        # should be the same! This indicates that the TNC callback may be
        # mutating something when it shouldn't.
        assert_allclose(res.x[[0, 2]], fd_res.x, rtol=2e-6)

