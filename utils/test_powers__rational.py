
def test_powers_Rational():
    """Test Rational._eval_power"""
    # check infinity
    assert S.Half ** S.Infinity == 0
    assert Rational(3, 2) ** S.Infinity is S.Infinity
    assert Rational(-1, 2) ** S.Infinity == 0
    assert Rational(-3, 2) ** S.Infinity == zoo

    # check Nan
    assert Rational(3, 4) ** S.NaN is S.NaN
    assert Rational(-2, 3) ** S.NaN is S.NaN

    # exact roots on numerator
    assert sqrt(Rational(4, 3)) == 2 * sqrt(3) / 3
    assert Rational(4, 3) ** Rational(3, 2) == 8 * sqrt(3) / 9
    assert sqrt(Rational(-4, 3)) == I * 2 * sqrt(3) / 3
    assert Rational(-4, 3) ** Rational(3, 2) == - I * 8 * sqrt(3) / 9
    assert Rational(27, 2) ** Rational(1, 3) == 3 * (2 ** Rational(2, 3)) / 2
    assert Rational(5**3, 8**3) ** Rational(4, 3) == Rational(5**4, 8**4)

    # exact root on denominator
    assert sqrt(Rational(1, 4)) == S.Half
    assert sqrt(Rational(1, -4)) == I * S.Half
    assert sqrt(Rational(3, 4)) == sqrt(3) / 2
    assert sqrt(Rational(3, -4)) == I * sqrt(3) / 2
    assert Rational(5, 27) ** Rational(1, 3) == (5 ** Rational(1, 3)) / 3

    # not exact roots
    assert sqrt(S.Half) == sqrt(2) / 2
    assert sqrt(Rational(-4, 7)) == I * sqrt(Rational(4, 7))
    assert Rational(-3, 2)**Rational(-7, 3) == \
        -4*(-1)**Rational(2, 3)*2**Rational(1, 3)*3**Rational(2, 3)/27
    assert Rational(-3, 2)**Rational(-2, 3) == \
        -(-1)**Rational(1, 3)*2**Rational(2, 3)*3**Rational(1, 3)/3
    assert Rational(-3, 2)**Rational(-10, 3) == \
        8*(-1)**Rational(2, 3)*2**Rational(1, 3)*3**Rational(2, 3)/81
    assert abs(Pow(Rational(-2, 3), Rational(-7, 4)).n() -
        Pow(Rational(-2, 3), Rational(-7, 4), evaluate=False).n()) < 1e-16

    # negative integer power and negative rational base
    assert Rational(-2, 3) ** Rational(-2, 1) == Rational(9, 4)

    a = Rational(1, 10)
    assert a**Float(a, 2) == Float(a, 2)**Float(a, 2)
    assert Rational(-2, 3)**Symbol('', even=True) == \
        Rational(2, 3)**Symbol('', even=True)

