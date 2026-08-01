
def test_sympy__codegen__ast__Node():
    from sympy.codegen.ast import Node
    assert _test_args(Node())
    assert _test_args(Node(attrs={1, 2, 3}))

