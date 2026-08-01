
def test_sympy__stats__stochastic_process_types__StochasticProcess():
    from sympy.stats.stochastic_process_types import StochasticProcess
    assert _test_args(StochasticProcess("Y", [1, 2, 3]))

