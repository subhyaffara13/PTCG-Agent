
def test_sympy__codegen__ast__Raise():
    from sympy.codegen.ast import Raise
    assert _test_args(Raise(x))

