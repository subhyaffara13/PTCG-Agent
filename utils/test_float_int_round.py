
def test_float_int_round():
    assert int(float(sqrt(10))) == int(sqrt(10))
    assert int(pi**1000) % 10 == 2
    assert int(Float('1.123456789012345678901234567890e20', '')) == \
        int(112345678901234567890)
    assert int(Float('1.123456789012345678901234567890e25', '')) == \
        int(11234567890123456789012345)
    # decimal forces float so it's not an exact integer ending in 000000
    assert int(Float('1.123456789012345678901234567890e35', '')) == \
        112345678901234567890123456789000192
    assert int(Float('123456789012345678901234567890e5', '')) == \
        12345678901234567890123456789000000
    assert Integer(Float('1.123456789012345678901234567890e20', '')) == \
        112345678901234567890
    assert Integer(Float('1.123456789012345678901234567890e25', '')) == \
        11234567890123456789012345
    # decimal forces float so it's not an exact integer ending in 000000
    assert Integer(Float('1.123456789012345678901234567890e35', '')) == \
        112345678901234567890123456789000192
    assert Integer(Float('123456789012345678901234567890e5', '')) == \
        12345678901234567890123456789000000
    assert same_and_same_prec(Float('123000e-2',''), Float('1230.00', ''))
    assert same_and_same_prec(Float('123000e2',''), Float('12300000', ''))

    assert int(1 + Rational('.9999999999999999999999999')) == 1
    assert int(pi/1e20) == 0
    assert int(1 + pi/1e20) == 1
    assert int(Add(1.2, -2, evaluate=False)) == int(1.2 - 2)
    assert int(Add(1.2, +2, evaluate=False)) == int(1.2 + 2)
    assert int(Add(1 + Float('.99999999999999999', ''), evaluate=False)) == 1
    raises(TypeError, lambda: float(x))
    raises(TypeError, lambda: float(sqrt(-1)))

    assert int(12345678901234567890 + cos(1)**2 + sin(1)**2) == \
        12345678901234567891

