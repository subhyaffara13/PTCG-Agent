
def test_sympy__codegen__ast__IntBaseType():
    from sympy.codegen.ast import IntBaseType
    assert _test_args(IntBaseType('bigint'))

