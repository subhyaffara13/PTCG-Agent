
def test_sympy__core__symbol__Wild():
    from sympy.core.symbol import Wild
    assert _test_args(Wild('x', exclude=[x]))

