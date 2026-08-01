
def test_sympy__codegen__fnodes__Subroutine():
    from sympy.codegen.fnodes import Subroutine
    x = symbols('x', real=True)
    assert _test_args(Subroutine('foo', [x], []))

