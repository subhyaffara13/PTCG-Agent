
def test_sympy__stats__matrix_distributions__MatrixGammaDistribution():
    from sympy.stats.matrix_distributions import MatrixGammaDistribution
    from sympy.matrices.dense import Matrix
    assert _test_args(MatrixGammaDistribution(3, 4, Matrix([[1, 0], [0, 1]])))

