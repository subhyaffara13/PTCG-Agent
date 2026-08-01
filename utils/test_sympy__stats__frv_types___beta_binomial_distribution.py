
def test_sympy__stats__frv_types__BetaBinomialDistribution():
    from sympy.stats.frv_types import BetaBinomialDistribution
    assert _test_args(BetaBinomialDistribution(5, 1, 1))

