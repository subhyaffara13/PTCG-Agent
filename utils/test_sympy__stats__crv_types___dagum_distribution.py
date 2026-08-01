
def test_sympy__stats__crv_types__DagumDistribution():
    from sympy.stats.crv_types import DagumDistribution
    assert _test_args(DagumDistribution(1, 1, 1))

