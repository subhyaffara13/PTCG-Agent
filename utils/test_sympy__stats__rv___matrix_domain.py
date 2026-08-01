
def test_sympy__stats__rv__MatrixDomain():
    from sympy.stats.rv import MatrixDomain
    from sympy.matrices import MatrixSet
    from sympy.core.singleton import S
    assert _test_args(MatrixDomain(x, MatrixSet(2, 2, S.Reals)))

