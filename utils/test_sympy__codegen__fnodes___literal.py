
def test_sympy__codegen__fnodes___literal():
    from sympy.codegen.fnodes import _literal
    assert _test_args(_literal(1))

