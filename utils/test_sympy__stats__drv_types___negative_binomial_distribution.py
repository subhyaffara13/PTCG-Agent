
def test_sympy__stats__drv_types__NegativeBinomialDistribution():
    from sympy.stats.drv_types import NegativeBinomialDistribution
    assert _test_args(NegativeBinomialDistribution(.5, .5))

