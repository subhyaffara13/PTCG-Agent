
def test_sympy__stats__joint_rv_types__MultinomialDistribution():
    from sympy.stats.joint_rv_types import MultinomialDistribution
    assert _test_args(MultinomialDistribution(5, [0.5, 0.1, 0.3]))

