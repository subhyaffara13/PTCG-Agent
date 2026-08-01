
def test_sympy__functions__combinatorial__factorials__binomial():
    from sympy.functions.combinatorial.factorials import binomial
    assert _test_args(binomial(2, x))

