
def test_sympy__printing__rust__TypeCast():
    from sympy.printing.rust import TypeCast
    from sympy.codegen.ast import real
    assert _test_args(TypeCast(x, real))

