
def test_sympy__matrices__expressions__sets__MatrixSet():
    from sympy.matrices.expressions.sets import MatrixSet
    from sympy.core.singleton import S
    assert _test_args(MatrixSet(2, 2, S.Reals))

