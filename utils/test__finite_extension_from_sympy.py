
def test_FiniteExtension_from_sympy():
    # Test to_sympy/from_sympy
    K = FiniteExtension(Poly(x**3 + 1, x, domain=ZZ))
    xf = K(x)
    assert K.from_sympy(x) == xf
    assert K.to_sympy(xf) == x

