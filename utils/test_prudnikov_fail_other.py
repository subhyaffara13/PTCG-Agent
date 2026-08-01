
def test_prudnikov_fail_other():
    # 7.11.2

    # 7.12.1
    assert can_do([1, a], [b, 1 - 2*a + b])  # ???

    # 7.14.2
    assert can_do([Rational(-1, 2)], [S.Half, 1])  # struve
    assert can_do([1], [S.Half, S.Half])  # struve
    assert can_do([Rational(1, 4)], [S.Half, Rational(5, 4)])  # PFDD
    assert can_do([Rational(3, 4)], [Rational(3, 2), Rational(7, 4)])  # PFDD
    assert can_do([1], [Rational(1, 4), Rational(3, 4)])  # PFDD
    assert can_do([1], [Rational(3, 4), Rational(5, 4)])  # PFDD
    assert can_do([1], [Rational(5, 4), Rational(7, 4)])  # PFDD
    # TODO LOTS more

    # 7.15.2
    assert can_do([S.Half, 1], [Rational(3, 4), Rational(5, 4), Rational(3, 2)])  # PFDD
    assert can_do([S.Half, 1], [Rational(7, 4), Rational(5, 4), Rational(3, 2)])  # PFDD

    # 7.16.1
    assert can_do([], [Rational(1, 3), S(2/3)])  # PFDD
    assert can_do([], [Rational(2, 3), S(4/3)])  # PFDD
    assert can_do([], [Rational(5, 3), S(4/3)])  # PFDD

    # XXX this does not *evaluate* right??
    assert can_do([], [a, a + S.Half, 2*a - 1])

