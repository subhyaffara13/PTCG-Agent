
def test_event_dense_output_LSODA(num_parallel_threads):
    if num_parallel_threads > 1:
        pytest.skip('LSODA does not allow for concurrent execution')

    def event_lsoda(t, y):
        return y[0] - 2.02e-5

    rtol = 1e-3
    atol = 1e-6
    y0 = [0.05]
    t_span = [-2, 2]
    first_step = 1e-3
    res = solve_ivp(
        fun_event_dense_output_LSODA,
        t_span,
        y0,
        method="LSODA",
        dense_output=True,
        events=event_lsoda,
        first_step=first_step,
        max_step=1,
        rtol=rtol,
        atol=atol,
        jac=jac_event_dense_output_LSODA,
    )

    assert_equal(res.t[0], t_span[0])
    assert_equal(res.t[-1], t_span[-1])
    assert_allclose(first_step, np.abs(res.t[1] - t_span[0]))
    assert res.success
    assert_equal(res.status, 0)

    y_true = sol_event_dense_output_LSODA(res.t)
    e = compute_error(res.y, y_true, rtol, atol)
    assert_array_less(e, 5)

    tc = np.linspace(*t_span)
    yc_true = sol_event_dense_output_LSODA(tc)
    yc = res.sol(tc)
    e = compute_error(yc, yc_true, rtol, atol)
    assert_array_less(e, 5)

    assert_allclose(res.sol(res.t), res.y, rtol=1e-15, atol=1e-15)

