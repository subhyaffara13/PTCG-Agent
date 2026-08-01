
def test_sympy__stats__crv_types__GaussianInverseDistribution():
    from sympy.stats.crv_types import GaussianInverseDistribution
    assert _test_args(GaussianInverseDistribution(1, 1))

