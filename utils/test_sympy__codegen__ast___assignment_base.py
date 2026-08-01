
def test_sympy__codegen__ast__AssignmentBase():
    from sympy.codegen.ast import AssignmentBase
    assert _test_args(AssignmentBase(x, 1))

