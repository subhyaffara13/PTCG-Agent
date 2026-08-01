
def test_sympy__codegen__ast__ComplexBaseType():
    from sympy.codegen.ast import ComplexBaseType
    assert _test_args(ComplexBaseType('positive_cmplx'))

