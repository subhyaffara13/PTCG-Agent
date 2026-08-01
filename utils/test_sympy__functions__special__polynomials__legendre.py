
def test_sympy__functions__special__polynomials__legendre():
    from sympy.functions.special.polynomials import legendre
    assert _test_args(legendre(x, 2))

