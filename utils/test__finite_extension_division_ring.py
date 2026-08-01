
def test_FiniteExtension_division_ring():
    # Test division in FiniteExtension over a ring
    KQ = FiniteExtension(Poly(x**2 - 1, x, domain=QQ))
    KZ = FiniteExtension(Poly(x**2 - 1, x, domain=ZZ))
    KQt = FiniteExtension(Poly(x**2 - 1, x, domain=QQ[t]))
    KQtf = FiniteExtension(Poly(x**2 - 1, x, domain=QQ.frac_field(t)))
    assert KQ.is_Field is True
    assert KZ.is_Field is False
    assert KQt.is_Field is False
    assert KQtf.is_Field is True
    for K in KQ, KZ, KQt, KQtf:
        xK = K.convert(x)
        assert xK / K.one == xK
        assert xK // K.one == xK
        assert xK % K.one == K.zero
        raises(ZeroDivisionError, lambda: xK / K.zero)
        raises(ZeroDivisionError, lambda: xK // K.zero)
        raises(ZeroDivisionError, lambda: xK % K.zero)
        if K.is_Field:
            assert xK / xK == K.one
            assert xK // xK == K.one
            assert xK % xK == K.zero
        else:
            raises(NotImplementedError, lambda: xK / xK)
            raises(NotImplementedError, lambda: xK // xK)
            raises(NotImplementedError, lambda: xK % xK)

