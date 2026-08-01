
def test_sympy__stats__stochastic_process_types__BernoulliProcess():
    from sympy.stats.stochastic_process_types import BernoulliProcess
    assert _test_args(BernoulliProcess("B", 0.5, 1, 0))

