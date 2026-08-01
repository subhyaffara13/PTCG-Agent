
def test_sympy__codegen__ast__SignedIntType():
    from sympy.codegen.ast import SignedIntType
    assert _test_args(SignedIntType('int128_with_sign', 128))

