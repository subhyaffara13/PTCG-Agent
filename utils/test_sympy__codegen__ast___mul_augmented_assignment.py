
def test_sympy__codegen__ast__MulAugmentedAssignment():
    from sympy.codegen.ast import MulAugmentedAssignment
    assert _test_args(MulAugmentedAssignment(x, 1))

