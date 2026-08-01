
def test_sympy__functions__special__elliptic_integrals__elliptic_k():
    from sympy.functions.special.elliptic_integrals import elliptic_k as K
    assert _test_args(K(x))

