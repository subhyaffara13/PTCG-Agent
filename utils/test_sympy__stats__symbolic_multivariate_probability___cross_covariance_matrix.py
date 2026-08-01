
def test_sympy__stats__symbolic_multivariate_probability__CrossCovarianceMatrix():
    from sympy.stats import CrossCovarianceMatrix
    from sympy.stats.rv import RandomMatrixSymbol
    assert _test_args(CrossCovarianceMatrix(RandomMatrixSymbol('R', 3, 1),
                        RandomMatrixSymbol('X', 3, 1)))

