
def test_sympy__functions__combinatorial__numbers__udivisor_sigma():
    from sympy.functions.combinatorial.numbers import udivisor_sigma
    k = symbols('k', integer=True)
    n = symbols('n', integer=True)
    t = udivisor_sigma(n, k)
    assert _test_args(t)

