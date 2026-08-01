
def test_sympy__codegen__pynodes__List():
    from sympy.codegen.pynodes import List
    assert _test_args(List(1, 2, 3))

