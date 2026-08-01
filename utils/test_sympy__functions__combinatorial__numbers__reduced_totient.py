
def test_sympy__functions__combinatorial__numbers__reduced_totient():
    from sympy.functions.combinatorial.numbers import reduced_totient
    k = symbols('k', integer=True)
    t = reduced_totient(k)
    assert _test_args(t)

