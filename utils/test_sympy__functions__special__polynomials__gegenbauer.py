
def test_sympy__functions__special__polynomials__gegenbauer():
    from sympy.functions.special.polynomials import gegenbauer
    assert _test_args(gegenbauer(x, 2, 2))

