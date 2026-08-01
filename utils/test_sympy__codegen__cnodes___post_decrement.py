
def test_sympy__codegen__cnodes__PostDecrement():
    from sympy.codegen.cnodes import PostDecrement
    assert _test_args(PostDecrement(x))

