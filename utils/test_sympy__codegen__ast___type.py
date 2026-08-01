
def test_sympy__codegen__ast__Type():
    from sympy.codegen.ast import Type
    assert _test_args(Type('float128'))

