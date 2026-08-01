
def test_sympy__functions__special__polynomials__chebyshevt_root():
    from sympy.functions.special.polynomials import chebyshevt_root
    assert _test_args(chebyshevt_root(3, 2))

