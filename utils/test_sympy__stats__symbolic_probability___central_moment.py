
def test_sympy__stats__symbolic_probability__CentralMoment():
    from sympy.stats.symbolic_probability import CentralMoment
    from sympy.stats import Normal
    X = Normal('X', 0, 1)
    assert _test_args(CentralMoment(X, 2, X > 1))

