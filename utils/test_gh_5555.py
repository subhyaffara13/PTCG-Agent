
def test_gh_5555():
    root = 0.1

    def f(x):
        return x - root

    methods = [zeros.bisect, zeros.ridder]
    xtol = rtol = TOL
    for method in methods:
        res = method(f, -1e8, 1e7, xtol=xtol, rtol=rtol)
        assert_allclose(root, res, atol=xtol, rtol=rtol,
                        err_msg=f'method {method.__name__}')

