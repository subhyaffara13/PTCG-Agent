
def test_sympy__stats__stochastic_process_types__ContinuousTimeStochasticProcess():
    from sympy.stats.stochastic_process_types import ContinuousTimeStochasticProcess
    assert _test_args(ContinuousTimeStochasticProcess("Y", [1, 2, 3]))

