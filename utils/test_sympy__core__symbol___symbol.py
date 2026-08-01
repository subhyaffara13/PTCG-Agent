
def test_sympy__core__symbol__Symbol():
    from sympy.core.symbol import Symbol
    assert _test_args(Symbol('t'))

