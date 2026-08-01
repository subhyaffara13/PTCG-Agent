
def test_sympy__functions__special__polynomials__assoc_legendre():
    from sympy.functions.special.polynomials import assoc_legendre
    assert _test_args(assoc_legendre(x, 0, y))

