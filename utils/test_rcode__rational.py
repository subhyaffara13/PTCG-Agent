
def test_rcode_Rational():
    assert rcode(Rational(3, 7)) == "3.0/7.0"
    assert rcode(Rational(18, 9)) == "2"
    assert rcode(Rational(3, -7)) == "-3.0/7.0"
    assert rcode(Rational(-3, -7)) == "3.0/7.0"
    assert rcode(x + Rational(3, 7)) == "x + 3.0/7.0"
    assert rcode(Rational(3, 7)*x) == "(3.0/7.0)*x"

