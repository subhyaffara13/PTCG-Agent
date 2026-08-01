
def test_sympy__stats__frv_types__HypergeometricDistribution():
    from sympy.stats.frv_types import HypergeometricDistribution
    assert _test_args(HypergeometricDistribution(10, 5, 3))

