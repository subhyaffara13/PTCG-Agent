
def test_Float_eq():
    # Floats with different precision should not compare equal
    assert Float(.5, 10) != Float(.5, 11) != Float(.5, 1)
    # but floats that aren't exact in base-2 still
    # don't compare the same because they have different
    # underlying mpf values
    assert Float(.12, 3) != Float(.12, 4)
    assert Float(.12, 3) != .12
    assert 0.12 != Float(.12, 3)
    assert Float('.12', 22) != .12
    # issue 11707
    # but Float/Rational -- except for 0 --
    # are exact so Rational(x) = Float(y) only if
    # Rational(x) == Rational(Float(y))
    assert Float('1.1') != Rational(11, 10)
    assert Rational(11, 10) != Float('1.1')
    # coverage
    assert not Float(3) == 2
    assert not Float(3) == Float(2)
    assert not Float(3) == 3
    assert not Float(2**2) == S.Half
    assert Float(2**2) == 4.0
    assert not Float(2**-2) == 1
    assert Float(2**-1) == 0.5
    assert not Float(2*3) == 3
    assert not Float(2*3) == 0.5
    assert Float(2*3) == 6.0
    assert not Float(2*3) == 6
    assert not Float(2*3) == 8
    assert not Float(.75) == Rational(3, 4)
    assert Float(.75) == 0.75
    assert Float(5/18) == 5/18
    # 4473
    assert Float(2.) != 3
    assert not Float((0,1,-3)) == S.One/8
    assert Float((0,1,-3)) == 1/8
    assert Float((0,1,-3)) != S.One/9
    # 16196
    assert not 2 == Float(2)  # unlike Python
    assert t**2 != t**2.0

