
def test_array_rtol():
    # solve_ivp had a bug with array_like `rtol`; see gh-15482
    # check that it's fixed
    def f(t, y):
        return y[0], y[1]

    # no warning (or error) when `rtol` is array_like
    sol = solve_ivp(f, (0, 1), [1., 1.], rtol=[1e-1, 1e-1])
    err1 = np.abs(np.linalg.norm(sol.y[:, -1] - np.exp(1)))

    # warning when an element of `rtol` is too small
    with pytest.warns(UserWarning, match="At least one element..."):
        sol = solve_ivp(f, (0, 1), [1., 1.], rtol=[1e-1, 1e-16])
        err2 = np.abs(np.linalg.norm(sol.y[:, -1] - np.exp(1)))

    # tighter rtol improves the error
    assert err2 < err1

