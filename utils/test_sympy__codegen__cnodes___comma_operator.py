
def test_sympy__codegen__cnodes__CommaOperator():
    from sympy.codegen.cnodes import CommaOperator
    assert _test_args(CommaOperator(1, 2))

