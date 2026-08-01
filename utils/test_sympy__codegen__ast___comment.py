
def test_sympy__codegen__ast__Comment():
    from sympy.codegen.ast import Comment
    assert _test_args(Comment('this is a comment'))

