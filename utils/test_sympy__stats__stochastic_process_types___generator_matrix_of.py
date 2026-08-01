
def test_sympy__stats__stochastic_process_types__GeneratorMatrixOf():
    from sympy.stats.stochastic_process_types import GeneratorMatrixOf, ContinuousMarkovChain
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    DMC = ContinuousMarkovChain("Y")
    assert _test_args(GeneratorMatrixOf(DMC, MatrixSymbol('T', 3, 3)))

