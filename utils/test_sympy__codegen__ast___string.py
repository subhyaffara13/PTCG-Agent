
def test_sympy__codegen__ast__String():
    from sympy.codegen.ast import String
    assert _test_args(String('foobar'))

