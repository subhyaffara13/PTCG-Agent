
def test_sympy__stats__stochastic_process_types__CountingProcess():
    from sympy.stats.stochastic_process_types import CountingProcess
    assert _test_args(CountingProcess("C"))

