
def test_sympy__functions__combinatorial__numbers__totient():
    from sympy.functions.combinatorial.numbers import totient
    k = symbols('k', integer=True)
    t = totient(k)
    assert _test_args(t)

