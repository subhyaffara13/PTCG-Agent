
def test_sympy__codegen__numpy_nodes__logaddexp2():
    from sympy.codegen.numpy_nodes import logaddexp2
    assert _test_args(logaddexp2(x, y))

