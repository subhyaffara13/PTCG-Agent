
def test_sympy__stats__frv_types__IdealSolitonDistribution():
    from sympy.stats.frv_types import IdealSolitonDistribution
    assert _test_args(IdealSolitonDistribution(10))

