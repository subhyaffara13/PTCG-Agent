
def test_prudnikov_12():
    # 7.16
    assert can_do(
        [], [a, a + S.Half, 2*a], False)  # branches only agree for some z!
    assert can_do([], [a, a + S.Half, 2*a + 1], False)  # dito
    assert can_do([], [S.Half, a, a + S.Half])
    assert can_do([], [Rational(3, 2), a, a + S.Half])

    assert can_do([], [Rational(1, 4), S.Half, Rational(3, 4)])
    assert can_do([], [S.Half, S.Half, 1])
    assert can_do([], [S.Half, Rational(3, 2), 1])
    assert can_do([], [Rational(3, 4), Rational(3, 2), Rational(5, 4)])
    assert can_do([], [1, 1, Rational(3, 2)])
    assert can_do([], [1, 2, Rational(3, 2)])
    assert can_do([], [1, Rational(3, 2), Rational(3, 2)])
    assert can_do([], [Rational(5, 4), Rational(3, 2), Rational(7, 4)])
    assert can_do([], [2, Rational(3, 2), Rational(3, 2)])

