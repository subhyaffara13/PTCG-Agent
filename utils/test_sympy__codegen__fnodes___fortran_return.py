
def test_sympy__codegen__fnodes__FortranReturn():
    from sympy.codegen.fnodes import FortranReturn
    assert _test_args(FortranReturn(10))

