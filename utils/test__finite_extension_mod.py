
def test_FiniteExtension_mod():
    # Test mod
    K = FiniteExtension(Poly(x**3 + 1, x, domain=QQ))
    xf = K(x)
    assert (xf**2 - 1) % 1 == K.zero
    assert 1 % (xf**2 - 1) == K.zero
    assert (xf**2 - 1) / (xf - 1) == xf + 1
    assert (xf**2 - 1) // (xf - 1) == xf + 1
    assert (xf**2 - 1) % (xf - 1) == K.zero
    raises(ZeroDivisionError, lambda: (xf**2 - 1) % 0)
    raises(TypeError, lambda: xf % [])
    raises(TypeError, lambda: [] % xf)

    # Test mod over ring
    K = FiniteExtension(Poly(x**3 + 1, x, domain=ZZ))
    xf = K(x)
    assert (xf**2 - 1) % 1 == K.zero
    raises(NotImplementedError, lambda: (xf**2 - 1) % (xf - 1))

