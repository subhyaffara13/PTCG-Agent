
def test_sympy__stats__stochastic_process_types__WienerProcess():
    from sympy.stats.stochastic_process_types import WienerProcess
    assert _test_args(WienerProcess("X"))

