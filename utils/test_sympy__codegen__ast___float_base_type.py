
def test_sympy__codegen__ast__FloatBaseType():
    from sympy.codegen.ast import FloatBaseType
    assert _test_args(FloatBaseType('positive_real'))

