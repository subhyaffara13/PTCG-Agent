
def test_tbound_respected_oscillator(method):
    "Regression test for gh-9198"
    def reactions_func(t, y):
        if (t > 205):
            raise ValueError("Called outside interval")
        yprime = np.array([1.73307544e-02,
                           6.49376470e-06,
                           0.00000000e+00,
                           0.00000000e+00])
        return yprime

    def run_sim2(t_end, n_timepoints=10, shortest_delay_line=10000000):
        init_state = np.array([134.08298555, 138.82348612, 100., 0.])
        t0 = 100.0
        t1 = 200.0
        return solve_ivp(reactions_func,
                         (t0, t1),
                         init_state.copy(),
                         dense_output=True,
                         max_step=t1 - t0)
    result = run_sim2(1000, 100, 100)
    assert result.success

