
def test_solve_logarithm():
    y = Symbol('y')
    assert _solve_logarithm(log(x**y) - y*log(x), 0, x, S.Reals) == S.Reals
    y = Symbol('y', positive=True)
    assert _solve_logarithm(log(x)*log(y), 0, x, S.Reals) == FiniteSet(1)

