
def test_sympy__codegen__cnodes__PostIncrement():
    from sympy.codegen.cnodes import PostIncrement
    assert _test_args(PostIncrement(x))

