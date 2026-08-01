
def test_sympy__stats__symbolic_probability__Probability():
    from sympy.stats.symbolic_probability import Probability
    from sympy.stats import Normal
    X = Normal('X', 0, 1)
    assert _test_args(Probability(X > 0))

