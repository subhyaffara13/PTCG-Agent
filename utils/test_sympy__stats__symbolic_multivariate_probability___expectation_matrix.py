
def test_sympy__stats__symbolic_multivariate_probability__ExpectationMatrix():
    from sympy.stats import ExpectationMatrix
    from sympy.stats.rv import RandomMatrixSymbol
    assert _test_args(ExpectationMatrix(RandomMatrixSymbol('R', 2, 1)))

