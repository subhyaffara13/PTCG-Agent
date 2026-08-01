
def test_sympy__codegen__cnodes__PreDecrement():
    from sympy.codegen.cnodes import PreDecrement
    assert _test_args(PreDecrement(x))

