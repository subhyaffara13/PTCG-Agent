
def test_sympy__stats__stochastic_process_types__PoissonProcess():
    from sympy.stats.stochastic_process_types import PoissonProcess
    assert _test_args(PoissonProcess("X", 2))

