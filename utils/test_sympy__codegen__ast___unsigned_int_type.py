
def test_sympy__codegen__ast__UnsignedIntType():
    from sympy.codegen.ast import UnsignedIntType
    assert _test_args(UnsignedIntType('unt128', 128))

