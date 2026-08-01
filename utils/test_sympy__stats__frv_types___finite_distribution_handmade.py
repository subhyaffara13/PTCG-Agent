
def test_sympy__stats__frv_types__FiniteDistributionHandmade():
    from sympy.stats.frv_types import FiniteDistributionHandmade
    from sympy.core.containers import Dict
    assert _test_args(FiniteDistributionHandmade(Dict({1: 1})))

