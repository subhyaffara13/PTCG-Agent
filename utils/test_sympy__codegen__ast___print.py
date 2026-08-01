
def test_sympy__codegen__ast__Print():
    from sympy.codegen.ast import Print
    assert _test_args(Print([x, y]))
    assert _test_args(Print([x, y], "%d %d"))

