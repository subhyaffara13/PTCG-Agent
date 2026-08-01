
def test_t_eval_dense_output():
    rtol = 1e-3
    atol = 1e-6
    y0 = [1/3, 2/9]
    t_span = [5, 9]
    t_eval = np.linspace(t_span[0], t_span[1], 10)
    res = solve_ivp(fun_rational, t_span, y0, rtol=rtol, atol=atol,
                    t_eval=t_eval)
    res_d = solve_ivp(fun_rational, t_span, y0, rtol=rtol, atol=atol,
                      t_eval=t_eval, dense_output=True)
    assert_equal(res.t, t_eval)
    assert_(res.t_events is None)
    assert_(res.success)
    assert_equal(res.status, 0)

    assert_equal(res.t, res_d.t)
    assert_equal(res.y, res_d.y)
    assert_(res_d.t_events is None)
    assert_(res_d.success)
    assert_equal(res_d.status, 0)

    # if t and y are equal only test values for one case
    y_true = sol_rational(res.t)
    e = compute_error(res.y, y_true, rtol, atol)
    assert_(np.all(e < 5))

