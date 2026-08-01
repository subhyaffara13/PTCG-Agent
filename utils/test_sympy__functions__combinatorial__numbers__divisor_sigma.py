
def test_sympy__functions__combinatorial__numbers__divisor_sigma():
    from sympy.functions.combinatorial.numbers import divisor_sigma
    k = symbols('k', integer=True)
    n = symbols('n', integer=True)
    t = divisor_sigma(n, k)
    assert _test_args(t)

