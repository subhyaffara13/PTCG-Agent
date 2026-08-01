
def test_sympy__stats__matrix_distributions__MatrixNormalDistribution():
    from sympy.stats.matrix_distributions import MatrixNormalDistribution
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    L = MatrixSymbol('L', 1, 2)
    S1 = MatrixSymbol('S1', 1, 1)
    S2 = MatrixSymbol('S2', 2, 2)
    assert _test_args(MatrixNormalDistribution(L, S1, S2))

