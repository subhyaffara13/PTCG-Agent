
def test_sympy__stats__stochastic_process_types__DiscreteTimeStochasticProcess():
    from sympy.stats.stochastic_process_types import DiscreteTimeStochasticProcess
    assert _test_args(DiscreteTimeStochasticProcess("Y", [1, 2, 3]))

