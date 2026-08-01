
def test_sympy__codegen__numpy_nodes__maximum():
    from sympy.codegen.numpy_nodes import maximum
    assert _test_args(maximum(x, y, z))

