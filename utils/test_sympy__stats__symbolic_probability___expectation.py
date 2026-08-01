
def test_sympy__stats__symbolic_probability__Expectation():
    from sympy.stats.symbolic_probability import Expectation
    from sympy.stats import Normal
    X = Normal('X', 0, 1)
    assert _test_args(Expectation(X > 0))

