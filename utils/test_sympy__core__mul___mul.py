
def test_sympy__core__mul__Mul():
    from sympy.core.mul import Mul
    assert _test_args(Mul(2, x, y, z))

