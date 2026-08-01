
def test_gcd_numbers_vs_polys():
    assert isinstance(gcd(3, 9), Integer)
    assert isinstance(gcd(3*x, 9), Integer)

    assert gcd(3, 9) == 3
    assert gcd(3*x, 9) == 3

    assert isinstance(gcd(Rational(3, 2), Rational(9, 4)), Rational)
    assert isinstance(gcd(Rational(3, 2)*x, Rational(9, 4)), Rational)

    assert gcd(Rational(3, 2), Rational(9, 4)) == Rational(3, 4)
    assert gcd(Rational(3, 2)*x, Rational(9, 4)) == 1

    assert isinstance(gcd(3.0, 9.0), Float)
    assert isinstance(gcd(3.0*x, 9.0), Float)

    assert gcd(3.0, 9.0) == 1.0
    assert gcd(3.0*x, 9.0) == 1.0

    # partial fix of 20597
    assert gcd(Mul(2, 3, evaluate=False), 2) == 2

