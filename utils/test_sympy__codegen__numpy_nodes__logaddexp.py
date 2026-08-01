
def test_sympy__codegen__numpy_nodes__logaddexp():
    from sympy.codegen.numpy_nodes import logaddexp
    assert _test_args(logaddexp(x, y))

