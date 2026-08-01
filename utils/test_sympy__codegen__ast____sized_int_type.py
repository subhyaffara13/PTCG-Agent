
def test_sympy__codegen__ast___SizedIntType():
    from sympy.codegen.ast import _SizedIntType
    assert _test_args(_SizedIntType('int128', 128))

