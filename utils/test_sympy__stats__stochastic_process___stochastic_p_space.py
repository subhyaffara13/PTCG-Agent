
def test_sympy__stats__stochastic_process__StochasticPSpace():
    from sympy.stats.stochastic_process import StochasticPSpace
    from sympy.stats.stochastic_process_types import StochasticProcess
    from sympy.stats.frv_types import BernoulliDistribution
    assert _test_args(StochasticPSpace("Y", StochasticProcess("Y", [1, 2, 3]), BernoulliDistribution(S.Half, 1, 0)))

