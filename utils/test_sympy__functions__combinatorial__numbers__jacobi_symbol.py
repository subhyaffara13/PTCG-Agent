
def test_sympy__functions__combinatorial__numbers__jacobi_symbol():
    from sympy.functions.combinatorial.numbers import jacobi_symbol
    assert _test_args(jacobi_symbol(2, 3))

