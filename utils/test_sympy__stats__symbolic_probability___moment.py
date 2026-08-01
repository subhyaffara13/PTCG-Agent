
def test_sympy__stats__symbolic_probability__Moment():
    from sympy.stats.symbolic_probability import Moment
    from sympy.stats import Normal
    X = Normal('X', 0, 1)
    assert _test_args(Moment(X, 3, 2, X > 3))

