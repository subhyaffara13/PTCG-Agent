
def test_sympy__codegen__ast__For():
    from sympy.codegen.ast import For, CodeBlock, AddAugmentedAssignment
    from sympy.sets import Range
    assert _test_args(For(x, Range(10), CodeBlock(AddAugmentedAssignment(y, 1))))

