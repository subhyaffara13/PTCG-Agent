
def test_sympy__codegen__ast__AugmentedAssignment():
    from sympy.codegen.ast import AugmentedAssignment
    assert _test_args(AugmentedAssignment(x, 1))

