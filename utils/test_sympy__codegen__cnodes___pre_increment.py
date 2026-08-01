
def test_sympy__codegen__cnodes__PreIncrement():
    from sympy.codegen.cnodes import PreIncrement
    assert _test_args(PreIncrement(x))

