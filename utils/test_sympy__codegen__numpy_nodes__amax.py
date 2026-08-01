
def test_sympy__codegen__numpy_nodes__amax():
    from sympy.codegen.numpy_nodes import amax
    assert _test_args(amax(x))

