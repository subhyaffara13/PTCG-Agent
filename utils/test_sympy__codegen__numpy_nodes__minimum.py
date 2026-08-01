
def test_sympy__codegen__numpy_nodes__minimum():
    from sympy.codegen.numpy_nodes import minimum
    assert _test_args(minimum(x, y, z))

