
def test_sympy__stats__joint_rv_types__NormalGammaDistribution():
    from sympy.stats.joint_rv_types import NormalGammaDistribution
    assert _test_args(NormalGammaDistribution(1, 2, 3, 4))

