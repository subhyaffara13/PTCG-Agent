
def test_t_eval_early_event():
    def early_event(t, y):
        return t - 7

    early_event.terminal = True

    rtol = 1e-3
    atol = 1e-6
    y0 = [1/3, 2/9]
    t_span = [5, 9]
    t_eval = np.linspace(7.5, 9, 16)
    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                "The following arguments have no effect for a chosen solver: `jac`",
                UserWarning,
            )
            res = solve_ivp(fun_rational, t_span, y0, rtol=rtol, atol=atol,
                            method=method, t_eval=t_eval, events=early_event,
                            jac=jac_rational)
        assert res.success
        assert res.message == 'A termination event occurred.'
        assert res.status == 1
        assert not res.t and not res.y
        assert len(res.t_events) == 1
        assert res.t_events[0].size == 1
        assert res.t_events[0][0] == 7

