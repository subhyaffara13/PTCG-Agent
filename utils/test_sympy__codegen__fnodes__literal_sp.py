
def test_sympy__codegen__fnodes__literal_sp():
    from sympy.codegen.fnodes import literal_sp
    assert _test_args(literal_sp(1))

