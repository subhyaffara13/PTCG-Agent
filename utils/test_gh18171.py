
def test_gh18171(method):
    # gh-3089 and gh-8394 reported that bracketing solvers returned incorrect
    # results when they encountered NaNs. Check that `root_scalar` returns
    # normally but indicates that convergence was unsuccessful. See gh-18171.
    def f(x):
        f._count += 1
        return np.nan
    f._count = 0

    res = root_scalar(f, bracket=(0, 1), method=method)
    assert res.converged is False
    assert res.flag.startswith("The function value at x")
    assert res.function_calls == f._count
    assert str(res.root) in res.flag

