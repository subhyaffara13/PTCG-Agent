
def test_fcode_Rational():
    x = symbols('x')
    assert fcode(Rational(3, 7)) == "      3.0d0/7.0d0"
    assert fcode(Rational(18, 9)) == "      2"
    assert fcode(Rational(3, -7)) == "      -3.0d0/7.0d0"
    assert fcode(Rational(-3, -7)) == "      3.0d0/7.0d0"
    assert fcode(x + Rational(3, 7)) == "      x + 3.0d0/7.0d0"
    assert fcode(Rational(3, 7)*x) == "      (3.0d0/7.0d0)*x"

