
def test_sympy__stats__crv_types__KumaraswamyDistribution():
    from sympy.stats.crv_types import KumaraswamyDistribution
    assert _test_args(KumaraswamyDistribution(1, 1))

