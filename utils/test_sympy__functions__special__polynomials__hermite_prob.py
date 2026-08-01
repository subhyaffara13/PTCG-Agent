
def test_sympy__functions__special__polynomials__hermite_prob():
    from sympy.functions.special.polynomials import hermite_prob
    assert _test_args(hermite_prob(x, 2))

