
def test_sympy__codegen__ast__While():
    from sympy.codegen.ast import While, AddAugmentedAssignment
    assert _test_args(While(abs(x) < 1, [AddAugmentedAssignment(x, -1)]))

