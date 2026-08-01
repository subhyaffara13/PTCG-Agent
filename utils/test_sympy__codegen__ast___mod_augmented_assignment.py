
def test_sympy__codegen__ast__ModAugmentedAssignment():
    from sympy.codegen.ast import ModAugmentedAssignment
    assert _test_args(ModAugmentedAssignment(x, 1))

