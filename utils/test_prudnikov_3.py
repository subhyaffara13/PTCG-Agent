
def test_prudnikov_3():
    h = S.Half
    assert can_do([Rational(1, 4), Rational(3, 4)], [h])
    assert can_do([Rational(1, 4), Rational(3, 4)], [3*h])
    assert can_do([Rational(1, 3), Rational(2, 3)], [3*h])
    assert can_do([Rational(3, 4), Rational(5, 4)], [h])
    assert can_do([Rational(3, 4), Rational(5, 4)], [3*h])

