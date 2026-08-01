
def test_slow_general_univariate():
    r = rootof(x**5 - x**2 + 1, 0)
    assert solve(sqrt(x) + 1/root(x, 3) > 1) == \
        Or(And(0 < x, x < r**6), And(r**6 < x, x < oo))

