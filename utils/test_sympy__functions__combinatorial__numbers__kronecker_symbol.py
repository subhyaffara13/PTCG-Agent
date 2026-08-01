
def test_sympy__functions__combinatorial__numbers__kronecker_symbol():
    from sympy.functions.combinatorial.numbers import kronecker_symbol
    assert _test_args(kronecker_symbol(2, 3))

