
def test_sympy__matrices__expressions__special__ZeroMatrix():
    from sympy.matrices.expressions.special import ZeroMatrix
    assert _test_args(ZeroMatrix(3, 5))

