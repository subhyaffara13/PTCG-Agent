
def test_sympy__stats__crv_types__BetaPrimeDistribution():
    from sympy.stats.crv_types import BetaPrimeDistribution
    assert _test_args(BetaPrimeDistribution(1, 1))

