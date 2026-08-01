
def test_sympy__simplify__hyperexpand__G_Function():
    from sympy.simplify.hyperexpand import G_Function
    assert _test_args(G_Function([2], [1], [], []))

