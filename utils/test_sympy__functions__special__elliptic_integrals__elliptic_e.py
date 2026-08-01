
def test_sympy__functions__special__elliptic_integrals__elliptic_e():
    from sympy.functions.special.elliptic_integrals import elliptic_e as E
    assert _test_args(E(x))
    assert _test_args(E(x, y))

