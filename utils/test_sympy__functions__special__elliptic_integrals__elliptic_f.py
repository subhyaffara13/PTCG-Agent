
def test_sympy__functions__special__elliptic_integrals__elliptic_f():
    from sympy.functions.special.elliptic_integrals import elliptic_f as F
    assert _test_args(F(x, y))

