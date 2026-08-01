
def test_sympy__functions__special__polynomials__hermite():
    from sympy.functions.special.polynomials import hermite
    assert _test_args(hermite(x, 2))

