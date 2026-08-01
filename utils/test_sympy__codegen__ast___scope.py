
def test_sympy__codegen__ast__Scope():
    from sympy.codegen.ast import Scope, AddAugmentedAssignment
    assert _test_args(Scope([AddAugmentedAssignment(x, -1)]))

