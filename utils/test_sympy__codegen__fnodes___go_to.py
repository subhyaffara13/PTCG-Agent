
def test_sympy__codegen__fnodes__GoTo():
    from sympy.codegen.fnodes import GoTo
    assert _test_args(GoTo([10]))
    assert _test_args(GoTo([10, 20], x > 1))

