
def test_prudnikov_fail_3F2():
    assert can_do([a, a + Rational(1, 3), a + Rational(2, 3)], [Rational(1, 3), Rational(2, 3)])
    assert can_do([a, a + Rational(1, 3), a + Rational(2, 3)], [Rational(2, 3), Rational(4, 3)])
    assert can_do([a, a + Rational(1, 3), a + Rational(2, 3)], [Rational(4, 3), Rational(5, 3)])

    # page 421
    assert can_do([a, a + Rational(1, 3), a + Rational(2, 3)], [a*Rational(3, 2), (3*a + 1)/2])

    # pages 422 ...
    assert can_do([Rational(-1, 2), S.Half, S.Half], [1, 1])  # elliptic integrals
    assert can_do([Rational(-1, 2), S.Half, 1], [Rational(3, 2), Rational(3, 2)])
    # TODO LOTS more

    # PFDD
    assert can_do([Rational(1, 8), Rational(3, 8), 1], [Rational(9, 8), Rational(11, 8)])
    assert can_do([Rational(1, 8), Rational(5, 8), 1], [Rational(9, 8), Rational(13, 8)])
    assert can_do([Rational(1, 8), Rational(7, 8), 1], [Rational(9, 8), Rational(15, 8)])
    assert can_do([Rational(1, 6), Rational(1, 3), 1], [Rational(7, 6), Rational(4, 3)])
    assert can_do([Rational(1, 6), Rational(2, 3), 1], [Rational(7, 6), Rational(5, 3)])
    assert can_do([Rational(1, 6), Rational(2, 3), 1], [Rational(5, 3), Rational(13, 6)])
    assert can_do([S.Half, 1, 1], [Rational(1, 4), Rational(3, 4)])

