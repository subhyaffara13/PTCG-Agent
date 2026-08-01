
def test_sympy__codegen__ast__CodeBlock():
    from sympy.codegen.ast import CodeBlock, Assignment
    assert _test_args(CodeBlock(Assignment(x, 1), Assignment(y, 2)))

