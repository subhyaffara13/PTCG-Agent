
def test_sympy__codegen__numpy_nodes__amin():
    from sympy.codegen.numpy_nodes import amin
    assert _test_args(amin(x))

