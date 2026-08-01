
def test_sympy__codegen__cnodes__Label():
    from sympy.codegen.cnodes import Label
    assert _test_args(Label('early_exit'))

