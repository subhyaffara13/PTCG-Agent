
def test_sympy__codegen__ast__FloatType():
    from sympy.codegen.ast import FloatType
    assert _test_args(FloatType('float242', 242, nmant=142, nexp=99))

