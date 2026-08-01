
def test_glsl_code_Rational():
    assert glsl_code(Rational(3, 7)) == "3.0/7.0"
    assert glsl_code(Rational(18, 9)) == "2"
    assert glsl_code(Rational(3, -7)) == "-3.0/7.0"
    assert glsl_code(Rational(-3, -7)) == "3.0/7.0"

