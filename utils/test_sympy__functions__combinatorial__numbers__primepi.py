
def test_sympy__functions__combinatorial__numbers__primepi():
    from sympy.functions.combinatorial.numbers import primepi
    n = symbols('n')
    t = primepi(n)
    assert _test_args(t)

