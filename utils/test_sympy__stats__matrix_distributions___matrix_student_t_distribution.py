
def test_sympy__stats__matrix_distributions__MatrixStudentTDistribution():
    from sympy.stats.matrix_distributions import MatrixStudentTDistribution
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    v = symbols('v', positive=True)
    Omega = MatrixSymbol('Omega', 3, 3)
    Sigma = MatrixSymbol('Sigma', 1, 1)
    Location = MatrixSymbol('Location', 1, 3)
    assert _test_args(MatrixStudentTDistribution(v, Location, Omega, Sigma))

