
def test_sympy__stats__symbolic_probability__Variance():
    from sympy.stats.symbolic_probability import Variance
    from sympy.stats import Normal
    X = Normal('X', 0, 1)
    assert _test_args(Variance(X))

