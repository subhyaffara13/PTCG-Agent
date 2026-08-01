
def test_sympy__stats__stochastic_process_types__StochasticStateSpaceOf():
    from sympy.stats.stochastic_process_types import StochasticStateSpaceOf, DiscreteMarkovChain
    DMC = DiscreteMarkovChain("Y")
    assert _test_args(StochasticStateSpaceOf(DMC, [0, 1, 2]))

