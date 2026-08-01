
def test_sympy__stats__crv_types__PowerFunctionDistribution():
    from sympy.stats.crv_types import PowerFunctionDistribution
    assert _test_args(PowerFunctionDistribution(2,0,1))

