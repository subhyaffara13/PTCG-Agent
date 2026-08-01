
def test_ccode_Rational():
    assert ccode(Rational(3, 7)) == "3.0/7.0"
    assert ccode(Rational(3, 7), type_aliases={real: float80}) == "3.0L/7.0L"
    assert ccode(Rational(18, 9)) == "2"
    assert ccode(Rational(3, -7)) == "-3.0/7.0"
    assert ccode(Rational(3, -7), type_aliases={real: float80}) == "-3.0L/7.0L"
    assert ccode(Rational(-3, -7)) == "3.0/7.0"
    assert ccode(Rational(-3, -7), type_aliases={real: float80}) == "3.0L/7.0L"
    assert ccode(x + Rational(3, 7)) == "x + 3.0/7.0"
    assert ccode(x + Rational(3, 7), type_aliases={real: float80}) == "x + 3.0L/7.0L"
    assert ccode(Rational(3, 7)*x) == "(3.0/7.0)*x"
    assert ccode(Rational(3, 7)*x, type_aliases={real: float80}) == "(3.0L/7.0L)*x"

