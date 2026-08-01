
def test_sympy__stats__frv_types__DiscreteUniformDistribution():
    from sympy.stats.frv_types import DiscreteUniformDistribution
    from sympy.core.containers import Tuple
    assert _test_args(DiscreteUniformDistribution(Tuple(*list(range(6)))))

