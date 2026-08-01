
def test_sympy__codegen__scipy_nodes__powm1():
    from sympy.codegen.scipy_nodes import powm1
    assert _test_args(powm1(x, y))

