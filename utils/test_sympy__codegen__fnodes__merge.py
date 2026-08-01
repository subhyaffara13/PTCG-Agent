
def test_sympy__codegen__fnodes__merge():
    from sympy.codegen.fnodes import merge
    assert _test_args(merge(1, 2, Eq(x, 0)))

