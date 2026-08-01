
def test_sympy__functions__combinatorial__numbers__primeomega():
    from sympy.functions.combinatorial.numbers import primeomega
    n = symbols('n', integer=True)
    t = primeomega(n)
    assert _test_args(t)

