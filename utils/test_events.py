
def test_events(num_parallel_threads):
    def event_rational_1(t, y):
        return y[0] - y[1] ** 0.7

    def event_rational_2(t, y):
        return y[1] ** 0.6 - y[0]

    def event_rational_3(t, y):
        return t - 7.4

    event_rational_3.terminal = True

    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        if method == 'LSODA' and num_parallel_threads > 1:
            continue

        res = solve_ivp(fun_rational, [5, 8], [1/3, 2/9], method=method,
                        events=(event_rational_1, event_rational_2))
        assert_equal(res.status, 0)
        assert_equal(res.t_events[0].size, 1)
        assert_equal(res.t_events[1].size, 1)
        assert_(5.3 < res.t_events[0][0] < 5.7)
        assert_(7.3 < res.t_events[1][0] < 7.7)

        assert_equal(res.y_events[0].shape, (1, 2))
        assert_equal(res.y_events[1].shape, (1, 2))
        assert np.isclose(
            event_rational_1(res.t_events[0][0], res.y_events[0][0]), 0)
        assert np.isclose(
            event_rational_2(res.t_events[1][0], res.y_events[1][0]), 0)

        event_rational_1.direction = 1
        event_rational_2.direction = 1
        res = solve_ivp(fun_rational, [5, 8], [1 / 3, 2 / 9], method=method,
                        events=(event_rational_1, event_rational_2))
        assert_equal(res.status, 0)
        assert_equal(res.t_events[0].size, 1)
        assert_equal(res.t_events[1].size, 0)
        assert_(5.3 < res.t_events[0][0] < 5.7)
        assert_equal(res.y_events[0].shape, (1, 2))
        assert_equal(res.y_events[1].shape, (0,))
        assert np.isclose(
            event_rational_1(res.t_events[0][0], res.y_events[0][0]), 0)

        event_rational_1.direction = -1
        event_rational_2.direction = -1
        res = solve_ivp(fun_rational, [5, 8], [1 / 3, 2 / 9], method=method,
                        events=(event_rational_1, event_rational_2))
        assert_equal(res.status, 0)
        assert_equal(res.t_events[0].size, 0)
        assert_equal(res.t_events[1].size, 1)
        assert_(7.3 < res.t_events[1][0] < 7.7)
        assert_equal(res.y_events[0].shape, (0,))
        assert_equal(res.y_events[1].shape, (1, 2))
        assert np.isclose(
            event_rational_2(res.t_events[1][0], res.y_events[1][0]), 0)

        event_rational_1.direction = 0
        event_rational_2.direction = 0

        res = solve_ivp(fun_rational, [5, 8], [1 / 3, 2 / 9], method=method,
                        events=(event_rational_1, event_rational_2,
                                event_rational_3), dense_output=True)
        assert_equal(res.status, 1)
        assert_equal(res.t_events[0].size, 1)
        assert_equal(res.t_events[1].size, 0)
        assert_equal(res.t_events[2].size, 1)
        assert_(5.3 < res.t_events[0][0] < 5.7)
        assert_(7.3 < res.t_events[2][0] < 7.5)
        assert_equal(res.y_events[0].shape, (1, 2))
        assert_equal(res.y_events[1].shape, (0,))
        assert_equal(res.y_events[2].shape, (1, 2))
        assert np.isclose(
            event_rational_1(res.t_events[0][0], res.y_events[0][0]), 0)
        assert np.isclose(
            event_rational_3(res.t_events[2][0], res.y_events[2][0]), 0)

        res = solve_ivp(fun_rational, [5, 8], [1 / 3, 2 / 9], method=method,
                        events=event_rational_1, dense_output=True)
        assert_equal(res.status, 0)
        assert_equal(res.t_events[0].size, 1)
        assert_(5.3 < res.t_events[0][0] < 5.7)

        assert_equal(res.y_events[0].shape, (1, 2))
        assert np.isclose(
            event_rational_1(res.t_events[0][0], res.y_events[0][0]), 0)

        # Also test that termination by event doesn't break interpolants.
        tc = np.linspace(res.t[0], res.t[-1])
        yc_true = sol_rational(tc)
        yc = res.sol(tc)
        e = compute_error(yc, yc_true, 1e-3, 1e-6)
        assert_(np.all(e < 5))

        # Test that the y_event matches solution
        assert np.allclose(sol_rational(res.t_events[0][0]), res.y_events[0][0],
                           rtol=1e-3, atol=1e-6)

    # Test in backward direction.
    event_rational_1.direction = 0
    event_rational_2.direction = 0
    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        if method == 'LSODA' and num_parallel_threads > 1:
            continue

        res = solve_ivp(fun_rational, [8, 5], [4/9, 20/81], method=method,
                        events=(event_rational_1, event_rational_2))
        assert_equal(res.status, 0)
        assert_equal(res.t_events[0].size, 1)
        assert_equal(res.t_events[1].size, 1)
        assert_(5.3 < res.t_events[0][0] < 5.7)
        assert_(7.3 < res.t_events[1][0] < 7.7)

        assert_equal(res.y_events[0].shape, (1, 2))
        assert_equal(res.y_events[1].shape, (1, 2))
        assert np.isclose(
            event_rational_1(res.t_events[0][0], res.y_events[0][0]), 0)
        assert np.isclose(
            event_rational_2(res.t_events[1][0], res.y_events[1][0]), 0)

        event_rational_1.direction = -1
        event_rational_2.direction = -1
        res = solve_ivp(fun_rational, [8, 5], [4/9, 20/81], method=method,
                        events=(event_rational_1, event_rational_2))
        assert_equal(res.status, 0)
        assert_equal(res.t_events[0].size, 1)
        assert_equal(res.t_events[1].size, 0)
        assert_(5.3 < res.t_events[0][0] < 5.7)

        assert_equal(res.y_events[0].shape, (1, 2))
        assert_equal(res.y_events[1].shape, (0,))
        assert np.isclose(
            event_rational_1(res.t_events[0][0], res.y_events[0][0]), 0)

        event_rational_1.direction = 1
        event_rational_2.direction = 1
        res = solve_ivp(fun_rational, [8, 5], [4/9, 20/81], method=method,
                        events=(event_rational_1, event_rational_2))
        assert_equal(res.status, 0)
        assert_equal(res.t_events[0].size, 0)
        assert_equal(res.t_events[1].size, 1)
        assert_(7.3 < res.t_events[1][0] < 7.7)

        assert_equal(res.y_events[0].shape, (0,))
        assert_equal(res.y_events[1].shape, (1, 2))
        assert np.isclose(
            event_rational_2(res.t_events[1][0], res.y_events[1][0]), 0)

        event_rational_1.direction = 0
        event_rational_2.direction = 0

        res = solve_ivp(fun_rational, [8, 5], [4/9, 20/81], method=method,
                        events=(event_rational_1, event_rational_2,
                                event_rational_3), dense_output=True)
        assert_equal(res.status, 1)
        assert_equal(res.t_events[0].size, 0)
        assert_equal(res.t_events[1].size, 1)
        assert_equal(res.t_events[2].size, 1)
        assert_(7.3 < res.t_events[1][0] < 7.7)
        assert_(7.3 < res.t_events[2][0] < 7.5)

        assert_equal(res.y_events[0].shape, (0,))
        assert_equal(res.y_events[1].shape, (1, 2))
        assert_equal(res.y_events[2].shape, (1, 2))
        assert np.isclose(
            event_rational_2(res.t_events[1][0], res.y_events[1][0]), 0)
        assert np.isclose(
            event_rational_3(res.t_events[2][0], res.y_events[2][0]), 0)

        # Also test that termination by event doesn't break interpolants.
        tc = np.linspace(res.t[-1], res.t[0])
        yc_true = sol_rational(tc)
        yc = res.sol(tc)
        e = compute_error(yc, yc_true, 1e-3, 1e-6)
        assert_(np.all(e < 5))

        assert np.allclose(sol_rational(res.t_events[1][0]), res.y_events[1][0],
                           rtol=1e-3, atol=1e-6)
        assert np.allclose(sol_rational(res.t_events[2][0]), res.y_events[2][0],
                           rtol=1e-3, atol=1e-6)

