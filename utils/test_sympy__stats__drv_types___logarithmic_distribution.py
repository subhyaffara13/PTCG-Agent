
def test_sympy__stats__drv_types__LogarithmicDistribution():
    from sympy.stats.drv_types import LogarithmicDistribution
    assert _test_args(LogarithmicDistribution(.5))

