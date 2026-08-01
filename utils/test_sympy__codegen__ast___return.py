
def test_sympy__codegen__ast__Return():
    from sympy.codegen.ast import Return
    assert _test_args(Return(x))

