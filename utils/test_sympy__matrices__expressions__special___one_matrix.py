
def test_sympy__matrices__expressions__special__OneMatrix():
    from sympy.matrices.expressions.special import OneMatrix
    assert _test_args(OneMatrix(3, 5))

