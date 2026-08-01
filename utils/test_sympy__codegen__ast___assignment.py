
def test_sympy__codegen__ast__Assignment():
    from sympy.codegen.ast import Assignment
    assert _test_args(Assignment(x, y))

