
def test_sympy__stats__frv_types__BinomialDistribution():
    from sympy.stats.frv_types import BinomialDistribution
    assert _test_args(BinomialDistribution(5, S.Half, 1, 0))

