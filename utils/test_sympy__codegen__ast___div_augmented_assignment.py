
def test_sympy__codegen__ast__DivAugmentedAssignment():
    from sympy.codegen.ast import DivAugmentedAssignment
    assert _test_args(DivAugmentedAssignment(x, 1))

