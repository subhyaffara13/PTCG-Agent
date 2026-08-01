
def test_sympy__stats__joint_rv_types__NegativeMultinomialDistribution():
    from sympy.stats.joint_rv_types import NegativeMultinomialDistribution
    assert _test_args(NegativeMultinomialDistribution(5, [0.5, 0.1, 0.3]))

