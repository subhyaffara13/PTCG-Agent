
def test_FiniteExtension_exquo():
    # Test exquo
    K = FiniteExtension(Poly(x**4 + 1))
    xf = K(x)
    assert K.exquo(xf**2 - 1, xf - 1) == xf + 1

