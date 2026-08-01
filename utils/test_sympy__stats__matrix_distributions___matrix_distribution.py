
def test_sympy__stats__matrix_distributions__MatrixDistribution():
    from sympy.stats.matrix_distributions import MatrixDistribution
    from sympy.matrices.dense import Matrix
    assert _test_args(MatrixDistribution(1, Matrix([[1, 0], [0, 1]])))

