
def test_sympy__codegen__ast__RuntimeError_():
    from sympy.codegen.ast import RuntimeError_
    assert _test_args(RuntimeError_('"message"'))

