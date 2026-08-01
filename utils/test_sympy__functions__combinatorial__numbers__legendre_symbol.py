
def test_sympy__functions__combinatorial__numbers__legendre_symbol():
    from sympy.functions.combinatorial.numbers import legendre_symbol
    assert _test_args(legendre_symbol(2, 3))

