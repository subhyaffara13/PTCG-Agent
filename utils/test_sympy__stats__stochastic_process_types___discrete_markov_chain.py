
def test_sympy__stats__stochastic_process_types__DiscreteMarkovChain():
    from sympy.stats.stochastic_process_types import DiscreteMarkovChain
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    assert _test_args(DiscreteMarkovChain("Y", [0, 1, 2], MatrixSymbol('T', 3, 3)))

