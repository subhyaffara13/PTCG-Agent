
def test_args_single_value():
    def fun_with_arg(t, y, a):
        return a*y

    message = "Supplied 'args' cannot be unpacked."
    with pytest.raises(TypeError, match=message):
        solve_ivp(fun_with_arg, (0, 0.1), [1], args=-1)

    sol = solve_ivp(fun_with_arg, (0, 0.1), [1], args=(-1,))
    assert_allclose(sol.y[0, -1], np.exp(-0.1))

