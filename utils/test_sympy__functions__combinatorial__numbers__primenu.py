
def test_sympy__functions__combinatorial__numbers__primenu():
    from sympy.functions.combinatorial.numbers import primenu
    n = symbols('n', integer=True)
    t = primenu(n)
    assert _test_args(t)

