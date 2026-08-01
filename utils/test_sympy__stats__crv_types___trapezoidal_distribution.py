
def test_sympy__stats__crv_types__TrapezoidalDistribution():
    from sympy.stats.crv_types import TrapezoidalDistribution
    assert _test_args(TrapezoidalDistribution(1, 2, 3, 4))

