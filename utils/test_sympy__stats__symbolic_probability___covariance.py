
def test_sympy__stats__symbolic_probability__Covariance():
    from sympy.stats.symbolic_probability import Covariance
    from sympy.stats import Normal
    X = Normal('X', 0, 1)
    Y = Normal('Y', 0, 3)
    assert _test_args(Covariance(X, Y))

