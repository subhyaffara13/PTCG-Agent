
def test_sympy__functions__special__polynomials__chebyshevt():
    from sympy.functions.special.polynomials import chebyshevt
    assert _test_args(chebyshevt(x, 2))

