
def test_mul_zero_detection():
    nz = Dummy(real=True, zero=False)
    r = Dummy(extended_real=True)
    c = Dummy(real=False, complex=True)
    c2 = Dummy(real=False, complex=True)
    i = Dummy(imaginary=True)
    e = nz*r*c
    assert e.is_imaginary is None
    assert e.is_extended_real is None
    e = nz*c
    assert e.is_imaginary is None
    assert e.is_extended_real is False
    e = nz*i*c
    assert e.is_imaginary is False
    assert e.is_extended_real is None
    # check for more than one complex; it is important to use
    # uniquely named Symbols to ensure that two factors appear
    # e.g. if the symbols have the same name they just become
    # a single factor, a power.
    e = nz*i*c*c2
    assert e.is_imaginary is None
    assert e.is_extended_real is None

    # _eval_is_extended_real and _eval_is_zero both employ trapping of the
    # zero value so args should be tested in both directions and
    # TO AVOID GETTING THE CACHED RESULT, Dummy MUST BE USED

    # real is unknown
    def test(z, b, e):
        if z.is_zero and b.is_finite:
            assert e.is_extended_real and e.is_zero
        else:
            assert e.is_extended_real is None
            if b.is_finite:
                if z.is_zero:
                    assert e.is_zero
                else:
                    assert e.is_zero is None
            elif b.is_finite is False:
                if z.is_zero is None:
                    assert e.is_zero is None
                else:
                    assert e.is_zero is False


    for iz, ib in product(*[[True, False, None]]*2):
        z = Dummy('z', nonzero=iz)
        b = Dummy('f', finite=ib)
        e = Mul(z, b, evaluate=False)
        test(z, b, e)
        z = Dummy('nz', nonzero=iz)
        b = Dummy('f', finite=ib)
        e = Mul(b, z, evaluate=False)
        test(z, b, e)

    # real is True
    def test(z, b, e):
        if z.is_zero and not b.is_finite:
            assert e.is_extended_real is None
        else:
            assert e.is_extended_real is True

    for iz, ib in product(*[[True, False, None]]*2):
        z = Dummy('z', nonzero=iz, extended_real=True)
        b = Dummy('b', finite=ib, extended_real=True)
        e = Mul(z, b, evaluate=False)
        test(z, b, e)
        z = Dummy('z', nonzero=iz, extended_real=True)
        b = Dummy('b', finite=ib, extended_real=True)
        e = Mul(b, z, evaluate=False)
        test(z, b, e)

