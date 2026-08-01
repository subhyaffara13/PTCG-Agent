
def test_sympy__stats__crv_types__ExGaussianDistribution():
    from sympy.stats.crv_types import ExGaussianDistribution
    assert _test_args(ExGaussianDistribution(1, 1, 1))

