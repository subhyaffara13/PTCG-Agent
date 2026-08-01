
def test_sympy__stats__stochastic_process_types__ContinuousMarkovChain():
    from sympy.stats.stochastic_process_types import ContinuousMarkovChain
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    assert _test_args(ContinuousMarkovChain("Y", [0, 1, 2], MatrixSymbol('T', 3, 3)))

