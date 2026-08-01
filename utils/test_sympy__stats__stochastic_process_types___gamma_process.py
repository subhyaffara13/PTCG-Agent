
def test_sympy__stats__stochastic_process_types__GammaProcess():
    from sympy.stats.stochastic_process_types import GammaProcess
    assert _test_args(GammaProcess("X", 1, 2))

