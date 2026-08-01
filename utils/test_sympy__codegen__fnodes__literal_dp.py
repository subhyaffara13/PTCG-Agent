
def test_sympy__codegen__fnodes__literal_dp():
    from sympy.codegen.fnodes import literal_dp
    assert _test_args(literal_dp(1))

