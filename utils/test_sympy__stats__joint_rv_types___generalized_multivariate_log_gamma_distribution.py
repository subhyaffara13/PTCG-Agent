
def test_sympy__stats__joint_rv_types__GeneralizedMultivariateLogGammaDistribution():
    from sympy.stats.joint_rv_types import GeneralizedMultivariateLogGammaDistribution
    v, l, mu = (4, [1, 2, 3, 4], [1, 2, 3, 4])
    assert _test_args(GeneralizedMultivariateLogGammaDistribution(S.Half, v, l, mu))

