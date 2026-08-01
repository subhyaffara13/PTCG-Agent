
def test_sympy__codegen__ast__AddAugmentedAssignment():
    from sympy.codegen.ast import AddAugmentedAssignment
    assert _test_args(AddAugmentedAssignment(x, 1))

