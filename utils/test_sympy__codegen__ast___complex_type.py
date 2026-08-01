
def test_sympy__codegen__ast__ComplexType():
    from sympy.codegen.ast import ComplexType
    assert _test_args(ComplexType('complex42', 42, nmant=15, nexp=5))

