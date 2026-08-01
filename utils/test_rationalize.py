
def test_rationalize():
    inputs = {
        '0.123': Rational(123, 1000)
    }
    transformations = standard_transformations + (rationalize,)
    for text, result in inputs.items():
        assert parse_expr(text, transformations=transformations) == result


def test_rationalize():
    from mpmath import cos, pi, mpf
    assert rationalize(cos(pi/3)) == S.Half
    assert rationalize(mpf("0.333333333333333")) == Rational(1, 3)
    assert rationalize(mpf("-0.333333333333333")) == Rational(-1, 3)
    assert rationalize(pi, maxcoeff = 250) == Rational(355, 113)

