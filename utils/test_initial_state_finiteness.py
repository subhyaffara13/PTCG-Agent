
def test_initial_state_finiteness(f0_fill):
    # regression test for gh-17846
    msg = "All components of the initial state `y0` must be finite."
    with pytest.raises(ValueError, match=msg):
        solve_ivp(fun_zero, [0, 10], np.full(3, f0_fill))

