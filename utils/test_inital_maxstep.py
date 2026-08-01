
def test_inital_maxstep():
    """Verify that select_inital_step respects max_step"""
    rtol = 1e-3
    atol = 1e-6
    y0 = np.array([1/3, 2/9])
    for (t0, t_bound) in ((5, 9), (5, 1)):
        for method_order in [RK23.error_estimator_order,
                            RK45.error_estimator_order,
                            DOP853.error_estimator_order,
                            3, #RADAU
                            1 #BDF
                            ]:
            step_no_max = select_initial_step(fun_rational, t0, y0, t_bound,
                                            np.inf,
                                            fun_rational(t0,y0),
                                            np.sign(t_bound - t0),
                                            method_order,
                                            rtol, atol)
            max_step = step_no_max/2
            step_with_max = select_initial_step(fun_rational, t0, y0, t_bound,
                                            max_step,
                                            fun_rational(t0, y0),
                                            np.sign(t_bound - t0),
                                            method_order,
                                            rtol, atol)
            assert_equal(max_step, step_with_max)

