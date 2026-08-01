
def test_sympy__codegen__ast__QuotedString():
    from sympy.codegen.ast import QuotedString
    assert _test_args(QuotedString('foobar'))

