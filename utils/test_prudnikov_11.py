
def test_prudnikov_11():
    # 7.15
    assert can_do([a, a + S.Half], [2*a, b, 2*a - b])
    assert can_do([a, a + S.Half], [Rational(3, 2), 2*a, 2*a - S.Half])

    assert can_do([Rational(1, 4), Rational(3, 4)], [S.Half, S.Half, 1])
    assert can_do([Rational(5, 4), Rational(3, 4)], [Rational(3, 2), S.Half, 2])
    assert can_do([Rational(5, 4), Rational(3, 4)], [Rational(3, 2), Rational(3, 2), 1])
    assert can_do([Rational(5, 4), Rational(7, 4)], [Rational(3, 2), Rational(5, 2), 2])

    assert can_do([1, 1], [Rational(3, 2), 2, 2])  # cosh-integral chi

