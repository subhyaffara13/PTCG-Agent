
def test_gh3089_8394(solver_name):
    # gh-3089 and gh-8394 reported that bracketing solvers returned incorrect
    # results when they encountered NaNs. Check that this is resolved.
    def f(x):
        return np.nan

    solver = getattr(zeros, solver_name)
    with pytest.raises(ValueError, match="The function value at x..."):
        solver(f, 0, 1)

