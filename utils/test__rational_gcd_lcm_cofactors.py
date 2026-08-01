
def test_Rational_gcd_lcm_cofactors():
    assert Integer(4).gcd(2) == Integer(2)
    assert Integer(4).lcm(2) == Integer(4)
    assert Integer(4).gcd(Integer(2)) == Integer(2)
    assert Integer(4).lcm(Integer(2)) == Integer(4)
    a, b = 720**99911, 480**12342
    assert Integer(a).lcm(b) == a*b/Integer(a).gcd(b)

    assert Integer(4).gcd(3) == Integer(1)
    assert Integer(4).lcm(3) == Integer(12)
    assert Integer(4).gcd(Integer(3)) == Integer(1)
    assert Integer(4).lcm(Integer(3)) == Integer(12)

    assert Rational(4, 3).gcd(2) == Rational(2, 3)
    assert Rational(4, 3).lcm(2) == Integer(4)
    assert Rational(4, 3).gcd(Integer(2)) == Rational(2, 3)
    assert Rational(4, 3).lcm(Integer(2)) == Integer(4)

    assert Integer(4).gcd(Rational(2, 9)) == Rational(2, 9)
    assert Integer(4).lcm(Rational(2, 9)) == Integer(4)

    assert Rational(4, 3).gcd(Rational(2, 9)) == Rational(2, 9)
    assert Rational(4, 3).lcm(Rational(2, 9)) == Rational(4, 3)
    assert Rational(4, 5).gcd(Rational(2, 9)) == Rational(2, 45)
    assert Rational(4, 5).lcm(Rational(2, 9)) == Integer(4)
    assert Rational(5, 9).lcm(Rational(3, 7)) == Rational(Integer(5).lcm(3),Integer(9).gcd(7))

    assert Integer(4).cofactors(2) == (Integer(2), Integer(2), Integer(1))
    assert Integer(4).cofactors(Integer(2)) == \
        (Integer(2), Integer(2), Integer(1))

    assert Integer(4).gcd(Float(2.0)) == Float(1.0)
    assert Integer(4).lcm(Float(2.0)) == Float(8.0)
    assert Integer(4).cofactors(Float(2.0)) == (Float(1.0), Float(4.0), Float(2.0))

    assert S.Half.gcd(Float(2.0)) == Float(1.0)
    assert S.Half.lcm(Float(2.0)) == Float(1.0)
    assert S.Half.cofactors(Float(2.0)) == \
        (Float(1.0), Float(0.5), Float(2.0))

