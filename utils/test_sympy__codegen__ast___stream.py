
def test_sympy__codegen__ast__Stream():
    from sympy.codegen.ast import Stream
    assert _test_args(Stream('stdin'))

