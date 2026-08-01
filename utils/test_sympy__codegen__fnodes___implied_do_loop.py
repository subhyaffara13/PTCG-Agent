
def test_sympy__codegen__fnodes__ImpliedDoLoop():
    from sympy.codegen.fnodes import ImpliedDoLoop
    assert _test_args(ImpliedDoLoop('i', 'i', 1, 42))

