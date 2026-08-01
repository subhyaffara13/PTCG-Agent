
def test_large_rational():
    e = (Rational(123712**12 - 1, 7) + Rational(1, 7))**Rational(1, 3)
    assert e == 234232585392159195136 * (Rational(1, 7)**Rational(1, 3))

