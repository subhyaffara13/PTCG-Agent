
def test_sympy__stats__stochastic_process_types__MarkovProcess():
    from sympy.stats.stochastic_process_types import MarkovProcess
    assert _test_args(MarkovProcess("Y", [1, 2, 3]))

