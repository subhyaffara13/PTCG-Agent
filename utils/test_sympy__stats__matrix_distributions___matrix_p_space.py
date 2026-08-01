
def test_sympy__stats__matrix_distributions__MatrixPSpace():
    from sympy.stats.matrix_distributions import MatrixDistribution, MatrixPSpace
    from sympy.matrices.dense import Matrix
    M = MatrixDistribution(1, Matrix([[1, 0], [0, 1]]))
    assert _test_args(MatrixPSpace('M', M, 2, 2))

