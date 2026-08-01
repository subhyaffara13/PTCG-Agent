
def test_sympy__stats__stochastic_process_types__TransitionMatrixOf():
    from sympy.stats.stochastic_process_types import TransitionMatrixOf, DiscreteMarkovChain
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    DMC = DiscreteMarkovChain("Y")
    assert _test_args(TransitionMatrixOf(DMC, MatrixSymbol('T', 3, 3)))

