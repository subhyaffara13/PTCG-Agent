
def test_sympy__codegen__ast__FunctionCall():
    from sympy.codegen.ast import FunctionCall
    assert _test_args(FunctionCall('pwer', [x]))

