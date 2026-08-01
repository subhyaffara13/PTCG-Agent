
def test_sympy__codegen__cnodes__goto():
    from sympy.codegen.cnodes import goto
    assert _test_args(goto('early_exit'))

