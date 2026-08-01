
def test_sympy__codegen__fnodes__FFunction():
    from sympy.codegen.fnodes import FFunction
    assert _test_args(FFunction('f'))

