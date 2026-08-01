
def test_sympy__codegen__ast__SubAugmentedAssignment():
    from sympy.codegen.ast import SubAugmentedAssignment
    assert _test_args(SubAugmentedAssignment(x, 1))

