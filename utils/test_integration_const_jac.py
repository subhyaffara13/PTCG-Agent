
def test_integration_const_jac():
    rtol = 1e-3
    atol = 1e-6
    y0 = [0, 2]
    t_span = [0, 2]
    J = jac_linear()
    J_sparse = csc_array(J)

    for method, jac in product(['Radau', 'BDF'], [J, J_sparse]):
        res = solve_ivp(fun_linear, t_span, y0, rtol=rtol, atol=atol,
                        method=method, dense_output=True, jac=jac)
        assert_equal(res.t[0], t_span[0])
        assert_(res.t_events is None)
        assert_(res.y_events is None)
        assert_(res.success)
        assert_equal(res.status, 0)

        assert_(res.nfev < 100)
        assert_equal(res.njev, 0)
        assert_(0 < res.nlu < 15)

        y_true = sol_linear(res.t)
        e = compute_error(res.y, y_true, rtol, atol)
        assert_(np.all(e < 10))

        tc = np.linspace(*t_span)
        yc_true = sol_linear(tc)
        yc = res.sol(tc)

        e = compute_error(yc, yc_true, rtol, atol)
        assert_(np.all(e < 15))

        assert_allclose(res.sol(res.t), res.y, rtol=1e-14, atol=1e-14)

