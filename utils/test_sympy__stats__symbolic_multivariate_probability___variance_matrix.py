
def test_sympy__stats__symbolic_multivariate_probability__VarianceMatrix():
    from sympy.stats import VarianceMatrix
    from sympy.stats.rv import RandomMatrixSymbol
    assert _test_args(VarianceMatrix(RandomMatrixSymbol('R', 3, 1)))

